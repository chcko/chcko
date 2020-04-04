# -*- coding: utf-8 -*-

import os
import re
import pytest
import datetime
import time

import chcko

from chcko.chcko import bottle
bottle.DEBUG = True
bottle.TEMPLATES.clear()
from chcko.chcko.tests.boddle import boddle

from chcko.chcko.languages import languages
from chcko.chcko.hlp import Struct, resolver, AUTHORDIRS
from chcko.chcko.tests.boddle import clear_all_data

@pytest.fixture
def cdb(db):
    with db.dbclient.context():
        clear_all_data(db)
    with db.dbclient.context():
        yield db

def _problems(authordir):
    for p,d,f in os.walk(authordir):
        authorid = os.path.basename(authordir)
        for problemid in d:
            if not problemid.startswith('_') and os.path.exists(os.path.join(p,problemid,'__init__.py')):
                yield '.'.join([authorid,problemid])
        del d[:]

def problems_for(student,cdb):
    for authordir in AUTHORDIRS:
        for pi in _problems(authordir):
            if pi not in {'r.'+x for x in 'abiu'}: continue #ndb slow
            rsv = resolver(pi, 'de')
            problem, pkwargs = cdb.problem_from_resolver(rsv, 1, student)
            assert problem
            cdb.set_answer(problem, problem.results)
            problem.answered = datetime.datetime.now()
            problem.oks = [True] * len(problem.results)
            cdb.save(problem)

def allcontent():
    for authordir in AUTHORDIRS:
        for pi in _problems(authordir):
            aidir = os.path.join(authordir, pi.split('.')[1])
            for ff in os.listdir(aidir):
                m = re.match('_*([a-z]+)\.html', ff)
                if m and m.group(1) in languages:
                    yield (pi, m.group(1),lambda x:True)

@pytest.fixture(params=[
    ('chcko.tests.t_1','en',
        lambda x:x==u'Here t_1.\nt_1 gets t_2:\nHere t_2.\nt_2 gets t_1:\nAfter.\nt_1 gets t_3:\nHere t_3.\nt_3 gets none.\n\n')
    ,('chcko.tests.t_3=3', 'en', lambda x:len(x.split('Here t_3.\nt_3 gets none.'))==4)
    ,('r.a&r.a1', 'en', lambda x:True) # mix problem and non-problem
    ,('r.b=2', 'en', lambda x:True) # more non-problems
]+list(allcontent()))
def newuserpage(request,cdb):
    query_string,lang,tst = request.param
    from chcko.chcko import contents
    user,_ = cdb.user_login('email@email.com',fullname='first last',password='password1',lang=lang)
    bddl=boddle(path=f'/{lang}/contents'
                ,user = user
                ,student = cdb.add_student(['-']*5)
                ,session = None
                ,lang = lang
                ,pagename = 'contents'
                ,environ = {'QUERY_STRING':f'{query_string}'}
                ,query=None
                )
    #bddl.__enter__()
    with bddl:
        assert bottle.request.user is not None
        assert bottle.request.student is not None
        newuserpage = cdb,contents.Page(contents),tst,query_string
        yield newuserpage

def test_recursive_includes(newuserpage):
    cdb,self,tst,q = newuserpage
    self.problem = None
    rr1 = self.load_content(
        rebase=False
        )  # via _new ...
    assert tst(rr1)
    assert self.problem is not None
    rr = self.load_content('chcko.tests.layout' if 'tests' in q else 'chcko.contents')  # and reload via _zip
    rrr = ''.join(rr)
    subs = q.split('&')
    if len(subs)>1:
        problem_set = list(cdb.problem_set(self.problem))
    else:
        problem_set = [self.problem]
    assert len(problem_set) == len(subs)
    if any([p.points for p in problem_set]):
        assert re.search('problemkey', rrr)
    else:
        assert not re.search('problemkey', rrr)

def test_depth_1st(cdb):
    path = ['a', 'b', 'c', 'd', 'e']
    student = cdb.add_student(path,None,'#EEE')
    problems_for(student,cdb)
    lst = list(cdb.depth_1st(path+[[]]))
    assert len(lst) >= 8
    lst = list(cdb.depth_1st(path+[[('query_string','=','r.u')]]))
    assert len(lst) == 6
    assert cdb.kindof(lst[0]) == 'School'
    assert cdb.kindof(lst[5]) == 'Problem'
    path = ['a', 'b', 'c', 'x', 'e'] #note same name for student
    student1 = cdb.add_student(path, None, '#EEE')
    problems_for(student1,cdb)
    path = ['a','b','c',[],[],[('query_string','=','r.u')]]
    lst = list(cdb.depth_1st(path))
    assert len(lst) == 9
    assert cdb.kindof(lst[0]) == 'School'
    assert cdb.kindof(lst[5]) == 'Problem'
    assert cdb.kindof(lst[6]) == 'Class'
    assert cdb.kindof(lst[7]) == 'Role'
    assert cdb.kindof(lst[8]) == 'Problem'
    lst = list(cdb.depth_1st(path,keys=cdb.keys_to_omit(path)))
    assert len(lst) == 6
    assert cdb.kindof(lst[0]) == 'Class'
    assert cdb.kindof(lst[2]) == 'Problem'
    assert cdb.kindof(lst[3]) == 'Class'
    assert cdb.kindof(lst[4]) == 'Role'
    assert cdb.kindof(lst[5]) == 'Problem'
    lst = list(cdb.depth_1st())
    assert lst == []

@pytest.fixture
def dbschool(request,db):
    '''returns
    {'Sc0':(Sc0,{'Fi0':(...)} }
    '''
    models = list(db.models.values())[:6]

    with db.dbclient.context():
        clear_all_data(db)

    def recursecreate(ient, thisent):
        res = {}
        if ient < len(models) - 1:
            ent = models[ient]
            for i in range(2):
                name = db.kindof(ent)[:2] + str(i) #Sc0,Fi0,...
                tent = ent.get_or_insert(name, parent=thisent and thisent.key)
                res.setdefault(name, (tent, recursecreate(ient + 1, tent)))
        else:
            problems_for(thisent, db)
        return res

    with db.dbclient.context():
        school = recursecreate(0, None)
        yield db, school

    def recurserem():
        todelete=[]
        def _recurserem(dct):
            for e in dct.values():
                _recurserem(e[1])
                todelete.append(e[0].key)
        _recurserem(school)
        db.delete_keys(todelete)

    with db.dbclient.context():
        recurserem()

kinddepth = lambda tbl,db,nm: list(filter(
    lambda x: x != 5, [list(db.models.keys())[:6].index(nm(tbl[i]))
           for i in range(len(tbl))]))

def test_school_setup(dbschool):
    db,school=dbschool
    if db.is_sql():
        pytest.skip("ancestor not available for SQL")
    #school = school(finrequest)
    tbl = list(db.keys_below(school['Sc0'][0]))
    kinds = kinddepth(tbl,db,lambda x:x.kind())
    assert kinds == [
        0, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4,
        4, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4, 4]

def test_descendants(dbschool):
    db,school=dbschool
    if db.is_sql():
        pytest.skip("ancestor not available for SQL")
    #school = school(finrequest)
    cla = db.key_from_path(['Sc1', 'Fi1', 'Te1', 'Cl1']).get()
    tbl = list(db.keys_below(cla))
    assert kinddepth(tbl,db,lambda x:x.kind()) == [3, 4, 4]
    # compare latter to this
    tbl = list(db.depth_1st(path=['Sc1', 'Fi1', 'Te1', 'Cl1']))
    assert kinddepth(tbl,db,lambda x:db.kindof(x)) == [0, 1, 2, 3, 4, 4]

def test_find_identities(dbschool):
    '''find all students with name Ro1'''
    db,school=dbschool
    #school = school(finrequest)
    _students = lambda tbl: [t for t in tbl if db.kindof(t) == 'Role']
    tbl = list(db.depth_1st(path=['Sc1', 'Fi1', [], [], 'Ro1']))
    assert kinddepth(tbl,db,lambda x:db.kindof(x)) == [0, 1, 2, 3, 4, 3, 4, 2, 3, 4, 3, 4]
    stset = set([':'.join(e.key.flat()) for e in _students(tbl)])
    goodstset = set(['School:Sc1:Field:Fi1:Teacher:Te1:Class:Cl1:Role:Ro1',
                     'School:Sc1:Field:Fi1:Teacher:Te0:Class:Cl1:Role:Ro1',
                     'School:Sc1:Field:Fi1:Teacher:Te0:Class:Cl0:Role:Ro1',
                     'School:Sc1:Field:Fi1:Teacher:Te1:Class:Cl0:Role:Ro1'])
    assert stset == goodstset

def test_assign_student(dbschool):
    db,school=dbschool
    stu = db.key_from_path(['Sc1', 'Fi1', 'Te1', 'Cl1', 'Ro1'])
    db.assign_to_student(db.urlsafe(stu), 'r.i&r.u', 1)
    asses = list(db.assign_table(stu.get(), None))
    assert asses
    ass = asses[0]
    assert ass.query_string == 'r.i&r.u'

def test_assign_to_class(dbschool):
    db,school=dbschool
    #school = school(finrequest)
    classkey = db.key_from_path(['Sc0', 'Fi0', 'Te0', 'Cl0'])
    query_string = 'r.a&r.b'
    duedays = '2'
    for st in db.depth_1st(keys=[classkey], kinds='Class Role'.split()):
        stk = st.key
        assert stk.parent().string_id() == 'Cl0'
        db.assign_to_student(stk.urlsafe(), query_string, duedays)
        #eventually consistent only: make two tries
        assigned_1 =  db.student_assignments(st).count() == 1
        if not assigned_1:
            time.sleep(1)
            assigned_1 =  db.student_assignments(st).count() == 1
        assert assigned_1

