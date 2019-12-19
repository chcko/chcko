# -*- coding: utf-8 -*-

#from chcko.conftest import *

import os
import os.path
import datetime

from chcko.db import *
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
            problem, pkwargs = db.problem_from_resolver(rsv, 1, student)
            problem.answers = problem.results
            problem.answered = datetime.datetime.now()
            problem.oks = [True] * len(problem.results)
            problem.put()


def clear_all_data():
    # clear_all_data()
    db.clear_index()
    db.clear_assignments()
    db.clear_problems()
    db.clear_students()


