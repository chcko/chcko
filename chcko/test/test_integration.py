# -*- coding: utf-8 -*-

import os.path
import re
import bottle
import datetime

import pytest

@pytest.fixture(scope="module")
def db():
    import chcko.db as chckodb
    from chcko.ndb import Ndb
    adb = chckodb.use(Ndb())
    with adb.dbclient.context():
        yield adb

from chcko.test.hlp import clear_all_data, problems_for

bottle.DEBUG = True
bottle.TEMPLATES.clear()

def newuserpage(db,query_string, lang):
    from chcko.app import app
    from chcko.content import Page
    db.clear_problems()
    db.clear_students()
    request = bottle.request
    request.environ['PATH_INFO'] = '/' + lang + '/?' + query_string
    request.pagename = 'content'
    request.query_string = query_string
    request.lang = lang
    request.user = db.User.create('email@email.com','password1')
    request.session = None
    db.set_student(request)
    page = Page(request)
    return page

def test_recursive_includes(db):
    self = newuserpage(db,'test.t_1', 'en')
    self.problem = None
    rr1 = self.load_content(rebase=False)  # via _new
    content = u'Here t_1.\nt_1 gets t_2:\nHere t_2.\nt_2 gets t_1:\nAfter.\nt_1 gets t_3:\nHere t_3.\nt_3 gets none.\n\n'
    assert rr1 == content
    assert self.problem is not None
    rr = self.load_content('test.layout')  # and reload via _zip
    assert rr1 in rr


def test_more(db):
    self = newuserpage(db,'test.t_3=3', 'en')
    self.problem = None
    rr1 = self.load_content(rebase=False)
    assert len(rr1.split('Here t_3.\nt_3 gets none.')) == 4
    assert self.problem is not None
    rr = self.load_content('test.layout')
    assert rr1 in rr


def _test_content(db, q, lang):
    # q,lang='r.a&r.b','en'
    self = newuserpage(db,q, lang)
    self.problem = None
    rr1 = self.load_content(rebase=False)  # via _new
    assert self.problem is not None
    rr = self.load_content()  # using content layout and via _zip
    assert rr1 in rr
    # q='r.a&r.b'
    subs = q.split('&')
    if len(subs) > 1:
        problem_set = Problem.query(
            Problem.collection == self.problem.key).order(
            Problem.nr)
        assert len(list(problem_set)) == len(subs)
        if any([p.points for p in problem_set]):
            assert re.search('problemkey', ''.join(rr))
        else:
            assert not re.search('problemkey', ''.join(rr))
    else:
        if self.problem.points:
            assert re.search('problemkey', ''.join(rr))
        else:
            assert not re.search('problemkey', ''.join(rr))


def test_r_ab(db):  # mix problem and non-problem
    _test_content(db,'r.a&r.b', 'en')


def test_r_bb(db):  # more non-problems
    _test_content(db,'r.b=2', 'en')

# see allcontent in ../conftest.py


def test_all_single(db,allcontent):
    _test_content(db,*allcontent)


@pytest.fixture(scope="module")
def school(db,request):
    '''returns
    {'Sc0':(Sc0,{'Pe0':(...)}}
    '''
    clear_all_data()

    def recursecreate(ient, thisent):
        res = {}
        models = db.models.values()
        if ient < len(db.models) - 1:
            ent = models[ient]
            for i in range(2):
                name = db.nameof(ent)[:2] + str(i) #Sc0,Pe0,...
                tent = ent.get_or_insert(name, parent=thisent and thisent.key)
                res.setdefault(name, (tent, recursecreate(ient + 1, tent)))
        else:
            problems_for(thisent, skip=4)
        return res
    school = recursecreate(0, None)
    # recurserem()

    def recurserem(dct=school):
        for e in dct.values():
            recurserem(e[1])
            e[0].key.delete()
    request.addfinalizer(recurserem)
    return school

kinddepth = lambda tbl: filter(
    lambda x: x != 5, [db.problem_contexts.index(db.nameof(tbl[i]))
           for i in range(len(tbl))])



def tree_keys(parent): #only used in testing
    return ndb.Query(ancestor=parent.key).iter(keys_only=True)

#for sql:
#def tree_keys(parent): #only used in testing
#    for x in DBSession().query(parent.__class__.of == parent.ID).all():
#        yield x.key

def test_school_setup(db,school):
    #school = school(finrequest)
    tbl = list(db.tree_keys(school['Sc0'][0]))
    kinds = kinddepth(tbl)
    assert kinds == [
        0, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4,
        4, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4, 4]


def test_descendants(db,school):
    #school = school(finrequest)
    cla = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1']).get()
    tbl = list(db.tree_keys(cla))
    assert kinddepth(tbl) == [3, 4, 4]
    # compare latter to this
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', 'Te1', 'Cl1']))
    assert kinddepth(tbl) == [0, 1, 2, 3, 4, 4]


def test_find_identities(db,school):
    '''find all students with name St1'''
    #school = school(finrequest)
    _students = lambda tbl: [t for t in tbl if db.nameof(t) == 'Student']
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', [], [], 'St1']))
    assert kinddepth(tbl) == [0, 1, 2, 3, 4, 3, 4, 2, 3, 4, 3, 4]
    stset = set([':'.join(e.key.flat()) for e in _students(tbl)])
    goodstset = set(['School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl0:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl0:Student:St1'])
    assert stset == goodstset


def test_assign_student(db,school):
    stu = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1'])
    db.assign_to_student(stu.urlsafe(), 'r.i&r.u', 1)
    asses = list(db.assigntable(stu, None))
    assert asses
    ass = asses[0].get()
    assert ass.query_string == 'r.i&r.u'


def test_assign_to_class(db,school):
    #school = school(finrequest)
    classkey = db.key_from_path(['Sc0', 'Pe0', 'Te0', 'Cl0'])
    query_string = 'r.a&r.b'
    duedays = '2'
    for st in db.depth_1st(keys=[classkey], models='Class Student'.split()):
        stk = st.key
        db.assign_to_student(stk.urlsafe(), query_string, duedays)
        assert db.student_assignments(stk).count() == 1
