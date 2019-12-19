# -*- coding: utf-8 -*-

import os.path
import re
import bottle
import datetime

from chcko.db import *
from chcko.test.hlp import clear_all_data, problems_for

import pytest

bottle.DEBUG = True
bottle.TEMPLATES.clear()

def newuserpage(query_string, lang):
    from chcko.app import app
    from chcko.content import Page
    db.clear_problems()
    db.clear_students()
    request = bottle.request
    request.environ['PATH_INFO'] = '/' + lang + '/?' + query_string
    request.pagename = 'content'
    request.query_string = query_string
    request.lang = lang
    set_student(request)
    page = Page(request)
    return page

def test_recursive_includes():
    self = newuserpage('test.t_1', 'en')
    self.problem = None
    rr1 = self.load_content(rebase=False)  # via _new
    content = u'Here t_1.\nt_1 gets t_2:\nHere t_2.\nt_2 gets t_1:\nAfter.\nt_1 gets t_3:\nHere t_3.\nt_3 gets none.\n\n'
    assert rr1 == content
    assert self.problem is not None
    rr = self.load_content('test.layout')  # and reload via _zip
    assert rr1 in rr


def test_more():
    self = newuserpage('test.t_3=3', 'en')
    self.problem = None
    rr1 = self.load_content(rebase=False)
    assert len(rr1.split('Here t_3.\nt_3 gets none.')) == 4
    assert self.problem is not None
    rr = self.load_content('test.layout')
    assert rr1 in rr


def _test_content(q, lang):
    # q,lang='r.a&r.b','en'
    self = newuserpage(q, lang)
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


def test_r_ab():  # mix problem and non-problem
    _test_content('r.a&r.b', 'en')


def test_r_bb():  # more non-problems
    _test_content('r.b=2', 'en')

# see allcontent in ../conftest.py


def test_all_single(allcontent):
    _test_content(*allcontent)


@pytest.fixture(scope="module")
def school(request):
    '''returns
    {'Sc0':(Sc0,{'Pe0':(...)}}
    '''
    clear_all_data()

    def recursecreate(ient, thisent):
        res = {}
        models = db.models.values()
        if ient < len(.models) - 1:
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
    lambda x: x != 5, [db.problem_contexts.index(tbl[i].kind())
           for i in range(len(tbl))])


def filterstudents(tbl):
    return [t for t in tbl if t.kind() == 'Student']

# school

def test_school_setup(school):
    #school = school(finrequest)
    tbl = list(db.tree_keys(school['Sc0'][0]))
    kinds = kinddepth(tbl)
    assert kinds == [
        0, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4,
        4, 1, 2, 3, 4, 4, 3, 4, 4, 2, 3, 4, 4, 3, 4, 4]


def test_descendants(school):
    #school = school(finrequest)
    cla = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1']).get()
    tbl = list(db.tree_keys(cla))
    assert kinddepth(tbl) == [3, 4, 4]
    # compare latter to this
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', 'Te1', 'Cl1']))
    assert kinddepth(tbl) == [0, 1, 2, 3, 4, 4]


def test_find_identities(school):
    '''find all students with name St1'''
    #school = school(finrequest)
    tbl = list(db.depth_1st(path=['Sc1', 'Pe1', [], [], 'St1']))
    assert kinddepth(tbl) == [0, 1, 2, 3, 4, 3, 4, 2, 3, 4, 3, 4]
    stset = set([':'.join(e.flat()) for e in filterstudents(tbl)])
    goodstset = set(['School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl1:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te0:Class:Cl0:Student:St1',
                     'School:Sc1:Period:Pe1:Teacher:Te1:Class:Cl0:Student:St1'])
    assert stset == goodstset


def test_assign_student(school):
    stu = db.key_from_path(['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1'])
    db.assign_to_student(stu.urlsafe(), 'r.i&r.u', 1)
    asses = list(db.assigntable(stu, None))
    assert asses
    ass = asses[0].get()
    assert ass.query_string == 'r.i&r.u'


def test_assign_to_class(school):
    #school = school(finrequest)
    classkey = db.key_from_path(['Sc0', 'Pe0', 'Te0', 'Cl0'])
    query_string = 'r.a&r.b'
    duedays = '2'
    for st in db.depth_1st(keys=[classkey], models='Class Student'.split()):
        db.assign_to_student(st.urlsafe(), query_string, duedays)
        assert db.student_assignments(st).count() == 1
