# -*- coding: utf-8 -*-
'''
This initializes py.test.
'''

import sys
import os
import os.path
import pytest
import urllib
import time
from contextlib import contextmanager

THISPATH = os.path.dirname(__file__)
sys.path += [THISPATH]

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
        for env_var in env_lines:
            k,v = env_var.replace('export ','').split('=')
            os.environ[k] = v

        time.sleep(2)
        OK = ''
        while 'Ok' not in OK:
            try:
                OK = urllib.request.urlopen(os.environ['DATASTORE_HOST']).read().decode()
            except urllib.error.URLError:
                pass

        yield
    finally:
        cleanup(proc_start.pid)


# mark step-wise tests with: @pytest.mark.incremental
# http://stackoverflow.com/questions/12411431/pytest-how-to-skip-the-rest-of-tests-in-the-class-if-one-has-failed/12579625#12579625
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item
def pytest_runtest_setup(item):
    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        pytest.xfail("previous test failed (%s)" % previousfailed.name)


def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="ndb", help="A session cannot have both [Ndb] and Sql DB"
    )

@pytest.fixture(scope='session')
def db(request):
    backnd = request.config.getoption("--db")
    import chcko.db as chckodb
    if backnd == "ndb":
        with emulator():
            from chcko.ndb import Ndb
            db = chckodb.use(Ndb())
            with db.dbclient.context():
                db.init_db()
                yield db
    else: # backnd == "sql":
        dbfile = os.path.join(THISPATH,'chcko','sqlite.db')
        if os.path.exists(dbfile):
            os.remove(dbfile)
        from chcko.sql import Sql
        db = chckodb.use(Sql())
        with db.dbclient.context():
            db.init_db()
            yield db
    #cntx=db.dbclient.context()
    #cntx.__enter__()
    #cntx.__exit__(*sys.exc_info())

