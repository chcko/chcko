# -*- coding: utf-8 -*-
'''
This initializes py.test.
'''

import sys
import os
import os.path
import urllib.request
import urllib.error
import time
from contextlib import contextmanager

try:
    import pytest
    def abort():
        pytest.exit(1)
    xfail = pytest.xfail
    fixture = pytest.fixture
except: #for dev_appserver.py environment
    def abort():
        sys.exit(1)
    def xfail(*a, **ka):
        sys.exit(1)
    def fixture(*a, **ka):
        def wrapper(*p,**k):
            pass
        return wrapper

def syspath_uninstalled():
    d = os.path.dirname
    j = os.path.join
    a = os.path.abspath
    abovechcko = d(d(a(__file__)))
    chckodirs = set([chd for chd in os.listdir(abovechcko) if chd.startswith('chcko')])
    for chd in chckodirs:
        asyspath = j(abovechcko,chd)
        if asyspath not in sys.path:
            sys.path.insert(0,asyspath)
syspath_uninstalled()

os.environ['CHCKOTESTING'] = "yes"

# from
# /mnt/src/python-ndb/test_utils/test_utils/scripts/run_emulator.py
import argparse
import os
import subprocess
import psutil

_DS_READY_LINE = '[datastore] Dev App Server is now running.\n'
def cleanup(pid):
    proc = psutil.Process(pid)
    for child_proc in proc.children(recursive=True):
        try:
            child_proc.kill()
            child_proc.terminate()
        except psutil.NoSuchProcess:
            pass
    proc.terminate()
    proc.kill()
@contextmanager
def emulator():
    print()
    ap=[x.name() for x in psutil.process_iter(attrs=['name']) if 'datastore' in x.name()]
    proc_start = None
    if not ap:
        print('Starting datastore emulator ...')
        start_command = ('gcloud', 'beta', 'emulators', 'datastore', 'start', '--no-store-on-disk')
        proc_start = subprocess.Popen(start_command, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    try:
        env_init_command = ('gcloud', 'beta', 'emulators', 'datastore', 'env-init')
        proc_env = subprocess.Popen(env_init_command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        env_status = proc_env.wait()
        if env_status != 0:
            raise RuntimeError(env_status, proc_env.stderr.read())
        env_lines = proc_env.stdout.read().decode().strip().split('\n')
        try:
            for env_var in env_lines:
                k,v = env_var.replace('export ','').split('=')
                val = v.replace('::1','localhost')
                os.environ[k] = val
                print(k,val)
        except ValueError:
            print('chcko conftest.py emulator problem. This happens occasionally. If it persists, debug it.')
            abort()

        time.sleep(1)
        OK = ''
        notOK = 0
        while 'Ok' not in OK:
            time.sleep(0.3)
            try:
                emulatorURL = os.environ['DATASTORE_HOST']
                OK = urllib.request.urlopen(emulatorURL).read().decode()
                print(emulatorURL,OK)
            except urllib.error.URLError:
                notOK = notOK + 1
                if notOK == 10:
                    print('chcko conftest.py emulator start fails. Retry, else debug it or start separately.')
                    abort()
        yield
    finally:
        if proc_start:
            cleanup(proc_start.pid)


# mark step-wise tests with: @pytest.mark.incremental
# https://stackoverflow.com/questions/12411431/pytest-how-to-skip-the-rest-of-tests-in-the-class-if-one-has-failed/12579625#12579625
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item
def pytest_runtest_setup(item):
    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        xfail("previous test failed (%s)" % previousfailed.name)


def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="ndb", help="A session cannot have both [ndb] and sql DB"
    )

@fixture(scope='session')
def db(request):
    backnd = request.config.getoption("--db")
    import chcko.chcko.db as chckodb
    if backnd == "ndb":
        with emulator():
            from chcko.chcko.ndb import Ndb
            db = chckodb.use(Ndb())
            with db.dbclient.context():
                db.init_db()
            yield db
    else: # backnd == "sql":
        testdburl = os.path.join(os.path.dirname(__file__),'chcko.sqlite')
        if os.path.exists(testdburl):
            os.remove(testdburl)
        testdburl = "sqlite:///"+testdburl
        from chcko.chcko.sql import Sql
        db = chckodb.use(Sql(testdburl))
        with db.dbclient.context():
            db.init_db()
        yield db
    #cntx=db.dbclient.context()
    #cntx.__enter__()
    #cntx.__exit__(*sys.exc_info())

