# -*- coding: utf-8 -*-

#from chcko.conftest import *

import os
import os.path
import webapp2
import datetime

from chcko.model import (Assignment, Index, Problem, Student, Class,
                              Teacher, Period, School, set_student, delete_all, db)
from chcko.hlp import Struct, import_module, from_py, resolver


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


def problems_for(
        student,
        skip=2,
        startdir=os.path.dirname(
        os.path.dirname(__file__))
    ):
    skipc = 0
    for f in os.listdir(os.path.join(startdir, 'r')):
        if not f.startswith('_'):
            skipc = skipc + 1
            if skipc % skip != 0:
                continue
            rsv = resolver('r.' + f, 'de')
            problem, pkwargs = Problem.from_resolver(rsv, 1, student.key)
            problem.answers = problem.results
            problem.answered = datetime.datetime.now()
            problem.oks = [True] * len(problem.results)
            problem.put()


def clear_all_data():
    # clear_all_data()
    delete_all(Assignment.query())
    delete_all(Index.query())
    delete_all(Problem.query())
    delete_all(Student.query())
    delete_all(Class.query())
    delete_all(Teacher.query())
    delete_all(Period.query())
    delete_all(School.query())


def newuserpage(query_string, lang):
    from chcko.app import app
    from chcko.content import Page
    delete_all(Student.query())
    not_answered = Problem.gql("WHERE answered = NULL")
    delete_all(not_answered)
    # query_string,lang='r.a=3','de'
    blank = webapp2.Request.blank('/' + lang + '/?' + query_string)
    request, response = webapp2.RequestContext(app, blank.environ).__enter__()
    request.pagename = 'content'
    request.query_string = query_string
    request.lang = lang
    set_student(request)
    page = Page(request)
    return page
