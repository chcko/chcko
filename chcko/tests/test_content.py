# -*- coding: utf-8 -*-

import re
import pytest
import datetime
import time

from chcko import bottle
bottle.DEBUG = True
bottle.TEMPLATES.clear()
from chcko.tests.boddle import boddle

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

@pytest.fixture(scope='module')
def cdb(db):
    db.clear_all_data()
    return db

def problems_for(student,cdb
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
            problem, pkwargs = cdb.problem_from_resolver(rsv, 1, student)
            assert problem
            cdb.set_answer(problem, problem.results)
            problem.answered = datetime.datetime.now()
            problem.oks = [True] * len(problem.results)
            cdb.save(problem)

def allcontent():
    d = os.path.dirname
    root = d(d(__file__))
    for fn, full in ((fn, os.path.join(root, fn)) for fn in os.listdir(root) if author_folder(fn, True)):
        for fs in os.listdir(full):
            if re.match('[a-z]+', fs):
                contentf = os.path.join(full, fs)
                if os.path.isdir(contentf):
                    for ff in os.listdir(contentf):
                        m = re.match('_*([a-z]+)\.html', ff)
                        if m and m.group(1) in languages:
                            yield ('.'.join([fn, fs]), m.group(1),lambda x:True)


@pytest.fixture(params=[
    ('tests.t_1','en',
        lambda x:x==u'Here t_1.\nt_1 gets t_2:\nHere t_2.\nt_2 gets t_1:\nAfter.\nt_1 gets t_3:\nHere t_3.\nt_3 gets none.\n\n')
    ,('tests.t_3=3', 'en', lambda x:len(x.split('Here t_3.\nt_3 gets none.'))==4)
    ,('r.a&r.b', 'en', lambda x:True) # mix problem and non-problem
    ,('r.b=2', 'en', lambda x:True) # more non-problems
]+list(allcontent()))
def newuserpage(request,cdb):
    query_string,lang,tst = request.param
    bottle.SimpleTemplate.defaults["contextcolor"] = '#EEE'
    from chcko.content import Page
    user,_ = cdb.user_create('email@email.com','password1','first last')
    bddl=boddle(path=f'/{lang}/content'
                ,user = user
                ,student = cdb.add_student()
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
        newuserpage = cdb,Page(),tst,query_string
        yield newuserpage

def test_recursive_includes(newuserpage):
    cdb,self,tst,q = newuserpage
    self.problem = None
    rr1 = self.load_content(
        rebase=False
        )  # via _new ...
    assert tst(rr1)
    assert self.problem is not None
    rr = self.load_content('tests.layout' if 'tests' in q else 'content')  # and reload via _zip
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
    student = cdb.add_student(path, user=None, color='#EEE')
    problems_for(student,cdb)
    lst = list(cdb.depth_1st(path+[[]]))
    assert len(lst) > 10
    lst = list(cdb.depth_1st(path+[[('query_string','=','r.u')]]))
    assert len(lst) == 6
    assert cdb.kindof(lst[0]) == 'School'
    assert cdb.kindof(lst[5]) == 'Problem'
    path = ['a', 'b', 'c', 'x', 'e'] #note same name for student
    student1 = cdb.add_student(path, user=None, color='#EEE')
    problems_for(student1,cdb)
    path = ['a','b','c',[],[],[('query_string','=','r.u')]]
    lst = list(cdb.depth_1st(path))
    assert len(lst) == 9
    assert cdb.kindof(lst[0]) == 'School'
    assert cdb.kindof(lst[5]) == 'Problem'
    assert cdb.kindof(lst[6]) == 'Class'
    assert cdb.kindof(lst[7]) == 'Student'
    assert cdb.kindof(lst[8]) == 'Problem'
    lst = list(cdb.depth_1st(path,keys=cdb.keys_to_omit(path)))
    assert len(lst) == 6
    assert cdb.kindof(lst[0]) == 'Class'
    assert cdb.kindof(lst[2]) == 'Problem'
    assert cdb.kindof(lst[3]) == 'Class'
    assert cdb.kindof(lst[4]) == 'Student'
    assert cdb.kindof(lst[5]) == 'Problem'
    lst = list(cdb.depth_1st())
    assert lst == []

@pytest.fixture(scope="module")
def dbschool(request,cdb):
    '''returns
    {'Sc0':(Sc0,{'Pe0':(...)} }
    '''
    cdb.clear_all_data()

    models = list(cdb.models.values())[:6]
    def recursecreate(ient, thisent):
        res = {}
        if ient < len(models) - 1:
            ent = models[ient]
            for i in range(2):
                name = cdb.kindof(ent)[:2] + str(i) #Sc0,Pe0,...
                tent = ent.get_or_insert(name, parent=thisent and thisent.key)
                res.setdefault(name, (tent, recursecreate(ient + 1, tent)))
        else:
            problems_for(thisent, cdb, skip=4)
        return res
    school = recursecreate(0, None)
    # recurserem()

    def recurserem():
        todelete=[]
        def _recurserem(dct):
            for e in dct.values():
                _recurserem(e[1])
                todelete.append(e[0].key)
        _recurserem(school)
        cdb.delete_keys(todelete)
    request.addfinalizer(recurserem)
    return cdb,school

kinddepth = lambda tbl,cdb,nm: list(filter(
    lambda x: x != 5, [list(cdb.models.keys())[:6].index(nm(tbl[i]))
           for i in range(len(tbl))]))

def test_school_setup(dbschool):
    cdb,school=dbschool
    if cdb.is_sql():
        pytest.skip("ancestor not available for SQL")
    #school = school(finrequest)
    tbl = list(cdb.keys_below(school['Sc0'][0]))
    kinds = kinddepth(tbl,cdb,lambda x:x.kind())
    assert kinds == [
        0, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4,
        4, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4, 4]

def test_descendants(dbschool):
    cdb,school=dbschool
    if cdb.is_sql():
        pytest.skip("ancestor not available for SQL")
    #school = school(finrequest)
    cla = cdb.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1']).get()
    tbl = list(cdb.keys_below(cla))
    assert kinddepth(tbl,cdb,lambda x:x.kind()) == [3, 4, 4]
    # compare latter to this
    tbl = list(cdb.depth_1st(path=['Sc1', 'Pe1', 'Te1', 'Cl1']))
    assert kinddepth(tbl,cdb,lambda x:cdb.kindof(x)) == [0, 1, 2, 3, 4, 4]

def test_find_identities(dbschool):
    '''find all students with name St1'''
    cdb,school=dbschool
    #school = school(finrequest)
    _students = lambda tbl: [t for t in tbl if cdb.kindof(t) == 'Student']
    tbl = list(cdb.depth_1st(path=['Sc1', 'Pe1', [], [], 'St1']))
    assert kinddepth(tbl,cdb,lambda x:cdb.kindof(x)) == [0, 1, 2, 3, 4, 3, 4, 2, 3, 4, 3, 4]
    stset = set([':'.join(e.key.flat()) for e in _students(tbl)])
    goodstset = set(['School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl0:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl0:Student:St1'])
    assert stset == goodstset

def test_assign_student(dbschool):
    cdb,school=dbschool
    stu = cdb.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1'])
    cdb.assign_to_student(cdb.urlsafe(stu), 'r.i&r.u', 1)
    asses = list(cdb.assign_table(stu.get(), None))
    assert asses
    ass = asses[0]
    assert ass.query_string == 'r.i&r.u'

def test_assign_to_class(dbschool):
    cdb,school=dbschool
    #school = school(finrequest)
    classkey = cdb.key_from_path(['Sc0', 'Pe0', 'Te0', 'Cl0'])
    query_string = 'r.a&r.b'
    duedays = '2'
    for st in cdb.depth_1st(keys=[classkey], kinds='Class Student'.split()):
        stk = st.key
        assert stk.parent().string_id() == 'Cl0'
        cdb.assign_to_student(stk.urlsafe(), query_string, duedays)
        #eventually consistent only: make two tries
        assigned_1 =  cdb.student_assignments(st).count() == 1
        if not assigned_1:
            time.sleep(1)
            assigned_1 =  cdb.student_assignments(st).count() == 1
        assert assigned_1

