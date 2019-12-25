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

from chcko.languages import languages
from chcko.hlp import author_folder

gaepath = '/opt/google-cloud-sdk/platform/google_appengine'
if not os.path.exists(gaepath):
    gaepath = os.path.expanduser('~/.local/opt/google-cloud-sdk/platform/google_appengine')

sys.path += [gaepath]

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


from subprocess import Popen
#prerequisite: gcloud config set project chcko-262117
datastore = Popen(['gcloud','beta','emulators','datastore','start'],env=os.environ)
@pytest.fixture(scope='session')
def gaetestbed(request):
    global datastore
    from chcko.db import *
    with datastore:
        #datastore.communicate(None, timeout=None)
        with db.dbclient.context():
            yield
    datastore.terminate()
    del datastore

def pytest_generate_tests(metafunc):
    if 'allcontent' in metafunc.fixturenames:
        root = os.path.dirname(__file__)

        def gen():
            for fn, full in ((fn, os.path.join(root, fn)) for fn in os.listdir(root) if author_folder(fn, True)):
                for fs in os.listdir(full):
                    if re.match('[a-z]+', fs):
                        contentf = os.path.join(full, fs)
                        for ff in os.listdir(contentf):
                            m = re.match('_*([a-z]+)\.html', ff)
                            if m and m.group(1) in languages:
                                yield ('.'.join([fn, fs]), m.group(1))
        # list(gen())
        metafunc.parametrize("allcontent", gen())

#import chcko.app
