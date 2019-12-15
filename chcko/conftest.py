# -*- coding: utf-8 -*-
'''
This initializes py.test.
'''

import sys
import os
import os.path
import pytest
import re

if 'google' in sys.modules:
    del sys.modules['google']

os.environ.update({'SERVER_SOFTWARE': 'py.test'})

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


tstbed = testbed.Testbed()
tstbed.activate()
tstbed.init_memcache_stub()
tstbed.init_datastore_v3_stub()
tstbed.init_mail_stub()

# init session

@pytest.fixture(scope='session')
def gaetestbed(request):
    def deactivate():
        tstbed.deactivate()
    request.addfinalizer(deactivate)
    return deactivate


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

import chcko.app
