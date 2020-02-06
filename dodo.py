# -*- coding: utf-8 -*-
'''
doit utility::

Do this after having changed an RST file.
Start this from chcko-x/chcko/::

    $ doit -kd. html

Do this after having changed the header (path, kind, level) in a html or rst file::

    $ doit initdb

Do this after any changes, especially in the main code::

    $ doit test
    $ doit cov

Do this to add new content, html or rst::

    $ doit -kd. new
    $ doit -kd. rst

task_included is internal.

'''

import os
import fnmatch
import sys
sys.path.insert(0,'.')

from chcko.chcko import doit_tasks

doit_tasks.set_base(__file__)

task_included = doit_tasks.task_included
task_html = doit_tasks.task_html
task_initdb = doit_tasks.task_initdb

CODE_FILES = [os.path.join(dirpath,f)
        for dirpath, dirnames, files in os.walk('chcko')
        for f in fnmatch.filter(files,'*.py')]
TEST_FILES = [os.path.join(dirpath,f)
        for dirpath, dirnames, files in os.walk('chcko')
        for f in fnmatch.filter(files,'test_*.py')]
PY_FILES = CODE_FILES + TEST_FILES
def run_test(test):
    return not bool(pytest.main(test))
def task_test():
    return {
        'actions':[
            ['py.test','chcko/chcko/tests','-vv','--db=sql'],
            ['py.test','chcko/chcko/tests','-vv','--db=ndb']
        ],
        'verbosity':2
    }
def task_cov():
    return {
        'actions':[
            ['py.test','chcko/chcko/tests','--cov','--db=sql'],
        ],
        'verbosity':2
    }
