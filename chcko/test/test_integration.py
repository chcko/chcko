# -*- coding: utf-8 -*-

import re
import pytest
import datetime

from chcko import bottle
bottle.DEBUG = True
bottle.TEMPLATES.clear()
from chcko.test.boddle import boddle

import os.path
from chcko.languages import languages
from chcko.hlp import author_folder, Struct, import_module, from_py, resolver


def check_test_answers(m=None, test_format=None):
    '''Call given, calc and norm once.
    Then apply norm to different test inputs.
    This verifies that none raises an exception.

    m can be module or __file__ or None

    For interactive use with globals:
    >>> test_format = [['2haa'],['2,2.2'],['2,2/2']]
    >>> check_test_answers(None,test_format)

    For use in a pytest test_xxx function
    >>> check_test_answers(__file__,test_format)

    '''
    if m is None:
        m = Struct()
        m.update(globals())
    elif isinstance(m, str):
        #m = __file__
        thisdir = os.path.dirname(os.path.abspath(m))
        sp = thisdir.split(os.sep)
        beyondmam = sp[sp.index('chcko') + 2:]
        if not beyondmam:
            return
        mn = os.path.join(*beyondmam).replace(os.sep, '.')
        m = import_module(mn)
    d = from_py(m)
    g = d.given()
    norm_results = d.norm(d.calc(g))
    if test_format:
        for t in test_format:
            d.norm(t)

def problems_for(student,db
        ,skip=2
        ,startdir=os.path.dirname(os.path.dirname(__file__))
    ):
    skipc = 0
    for f in os.listdir(os.path.join(startdir, 'r')):
        if not f.startswith('_'):
            skipc = skipc + 1
            if skipc % skip != 0:
                continue
            rsv = resolver('r.' + f, 'de')
            problem, pkwargs = db.problem_from_resolver(rsv, 1, student)
            problem.answers = problem.results
            problem.answered = datetime.datetime.now()
            problem.oks = [True] * len(problem.results)
            problem.put()

def allcontent():
    d = os.path.dirname
    root = d(d(__file__))
    for fn, full in ((fn, os.path.join(root, fn)) for fn in os.listdir(root) if author_folder(fn, True)):
        for fs in os.listdir(full):
            if re.match('[a-z]+', fs):
                contentf = os.path.join(full, fs)
                for ff in os.listdir(contentf):
                    m = re.match('_*([a-z]+)\.html', ff)
                    if m and m.group(1) in languages:
                        yield ('.'.join([fn, fs]), m.group(1),lambda x:True)


@pytest.fixture(params=[
    ('test.t_1','en',
        lambda x:x==u'Here t_1.\nt_1 gets t_2:\nHere t_2.\nt_2 gets t_1:\nAfter.\nt_1 gets t_3:\nHere t_3.\nt_3 gets none.\n\n')
    ,('test.t_3=3', 'en', lambda x:len(x.split('Here t_3.\nt_3 gets none.'))==4)
    ,('r.a&r.b', 'en', lambda x:True) # mix problem and non-problem
    ,('r.b=2', 'en', lambda x:True)# more non-problems
]+list(allcontent()))
def newuserpage(request,db):
    query_string,lang,tst = request.param
    bottle.SimpleTemplate.defaults["contextcolor"] = '#EEE'
    from chcko.content import Page
    bddl=boddle(path=f'/{lang}/content'
                ,user = db.user_create('email@email.com','password1')
                ,student = db.add_student()
                ,session = None
                ,lang = lang
                ,pagename = 'content'
                ,environ = {'QUERY_STRING':f'{query_string}'}
                ,query=None
                )
    #bddl.__enter__()
    with bddl:
        assert bottle.request.user is not None
        assert bottle.request.student is not None
        newuserpage = db,Page(bottle.request),tst,query_string
        yield newuserpage

def test_recursive_includes(newuserpage):
    db,self,tst,q = newuserpage
    self.problem = None
    rr1 = self.load_content(
        rebase=False
        )  # via _new ...
    assert tst(rr1)
    assert self.problem is not None
    rr = self.load_content('test.layout' if 'test' in q else 'content')  # and reload via _zip
    assert rr1 in rr
    rrr = ''.join(rr)
    subs = q.split('&')
    if len(subs)>1:
        problem_set = list(db.problem_set(self.problem))
    else:
        problem_set = [self.problem]
    assert len(problem_set) == len(subs)
    if any([p.points for p in problem_set]):
        assert re.search('problemkey', rrr)
    else:
        assert not re.search('problemkey', rrr)

def test_depth_1st(db):
    path = ['a', 'b', 'c', 'd', 'e']
    student = db.add_student(path, 'EEE')
    problems_for(student,db)
    lst = list(db.depth_1st(path+[[]]))
    assert len(lst) > 10
    lst = list(db.depth_1st(path+[[('query_string','=','r.u')]]))
    assert len(lst) == 6
    assert db.nameof(lst[0]) == 'School'
    assert db.nameof(lst[5]) == 'Problem'
    path = ['a', 'b', 'c', 'x', 'e'] #note same name for student
    student1 = db.add_student(path, 'EEE')
    problems_for(student1,db)
    path = ['a','b','c',[],[],[('query_string','=','r.u')]]
    lst = list(db.depth_1st(path))
    assert len(lst) == 9
    assert db.nameof(lst[0]) == 'School'
    assert db.nameof(lst[5]) == 'Problem'
    assert db.nameof(lst[6]) == 'Class'
    assert db.nameof(lst[7]) == 'Student'
    assert db.nameof(lst[8]) == 'Problem'
    lst = list(db.depth_1st(path,keys=db.keys_to_omit(path)))
    assert len(lst) == 6
    assert db.nameof(lst[0]) == 'Class'
    assert db.nameof(lst[2]) == 'Problem'
    assert db.nameof(lst[3]) == 'Class'
    assert db.nameof(lst[4]) == 'Student'
    assert db.nameof(lst[5]) == 'Problem'
    lst = list(db.depth_1st())
    assert lst == []

@pytest.fixture(scope="module")
def dbschool(request,db):
    '''returns
    {'Sc0':(Sc0,{'Pe0':(...)}}
    '''
    db.clear_all_data()

    models = list(db.models.values())[:6]
    def recursecreate(ient, thisent):
        res = {}
        if ient < len(models) - 1:
            ent = models[ient]
            for i in range(2):
                name = db.nameof(ent)[:2] + str(i) #Sc0,Pe0,...
                tent = ent.get_or_insert(name, parent=thisent and thisent.key)
                res.setdefault(name, (tent, recursecreate(ient + 1, tent)))
        else:
            problems_for(thisent, db, skip=4)
        return res
    school = recursecreate(0, None)
    # recurserem()

    def recurserem(dct=school):
        for e in dct.values():
            recurserem(e[1])
            e[0].key.delete()
    request.addfinalizer(recurserem)
    return db,school

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
    cla = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1']).get()
    tbl = list(db.keys_below(cla))
    assert kinddepth(tbl,db,lambda x:x.kind()) == [3, 4, 4]
    # compare latter to this
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', 'Te1', 'Cl1']))
    assert kinddepth(tbl,db,lambda x:db.nameof(x)) == [0, 1, 2, 3, 4, 4]


def test_find_identities(dbschool):
    '''find all students with name St1'''
    db,school=dbschool
    #school = school(finrequest)
    _students = lambda tbl: [t for t in tbl if db.nameof(t) == 'Student']
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', [], [], 'St1']))
    assert kinddepth(tbl,db,lambda x:db.nameof(x)) == [0, 1, 2, 3, 4, 3, 4, 2, 3, 4, 3, 4]
    stset = set([':'.join(e.key.flat()) for e in _students(tbl)])
    goodstset = set(['School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl0:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl0:Student:St1'])
    assert stset == goodstset

def test_assign_student(dbschool):
    db,school=dbschool
    stu = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1'])
    db.assign_to_student(stu.urlsafe(), 'r.i&r.u', 1)
    asses = list(db.assign_table(stu.get(), None))
    assert asses
    ass = asses[0]
    assert ass.query_string == 'r.i&r.u'

def test_assign_to_class(dbschool):
    db,school=dbschool
    #school = school(finrequest)
    classkey = db.key_from_path(['Sc0', 'Pe0', 'Te0', 'Cl0'])
    query_string = 'r.a&r.b'
    duedays = '2'
    for st in db.depth_1st(keys=[classkey], kinds='Class Student'.split()):
        stk = st.key
        db.assign_to_student(stk.urlsafe(), query_string, duedays)
        assert db.student_assignments(st).count() == 1

