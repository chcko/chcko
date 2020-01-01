# -*- coding: utf-8 -*-
'''
This initializes py.test.
'''

import sys
import os
import os.path
import pytest
import re

#if 'google' in sys.modules: del sys.modules['google']

os.environ.update({'SERVER_SOFTWARE': 'py.test'})
os.environ.update({'CLOUDSDK_CORE_PROJECT': 'chcko'})
os.environ.update({'DATASTORE_EMULATOR_HOST': 'localhost:8081'})

sys.path += [os.path.dirname(os.path.dirname(__file__))]

#gaepath = '/opt/google-cloud-sdk/platform/google_appengine'
#if not os.path.exists(gaepath):
#    gaepath = os.path.expanduser('~/.local/opt/google-cloud-sdk/platform/google_appengine')
#
#sys.path += [gaepath]

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

#from subprocess import Popen
##prerequisite: gcloud config set project chcko-262117
#datastore = Popen(['gcloud','beta','emulators','datastore','start'],env=os.environ)
#@pytest.fixture(scope='session')
#def gaetestbed(request):
#    global datastore
#    from chcko.db import db
#    with datastore:
#        #datastore.communicate(None, timeout=None)
#        with db.dbclient.context():
#            yield
#    datastore.terminate()
#    del datastore
@pytest.fixture(scope='session')
def db(request):
    backnd = request.config.getoption("--db")
    #backnd = "ndb"
    import chcko.db as chckodb
    if backnd == "ndb":
        from chcko.ndb import Ndb
        db = chckodb.use(Ndb())
        #TODO: assert that data store emulator is running
    elif backnd == "sql":
        from chcko.sql import Sql
        db = chckodb.use(Sql())
    cntx=db.dbclient.context()
    #cntx.__enter__()
    #cntx.__exit__(*sys.exc_info())
    with cntx:
        yield db

#import chcko.app
