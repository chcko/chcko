"""
Contains entry point ``app`` for google cloud platform.
"""


import os
if os.getenv('GAE_ENV', '').startswith('standard'):
    pass
    # ## depends on imports in : requirements.txt
    # try:
    #   import googleclouddebugger
    #   googleclouddebugger.enable()
    # except ImportError:
    #   pass
    # ## needs logging permission
    # try:
    #   import google.cloud.logging
    #   logger = google.cloud.logging.Client()
    #   logger.setup_logging()
    # except ImportError:
    #   pass
else:
    # $1: gcloud beta emulators datastore start --no-store-on-disk --data-dir .
    # $2: cd .. && python2 `which dev_appserver.py` chcko
    import sys
    if sys.path[0] != '.':
        sys.path.insert(0,'.')
    from conftest import emulator
    emulator().__enter__()

from chcko.chcko.db import use
from chcko.chcko.ndb import Ndb
db = Ndb()
with db.dbclient.context():
    db.init_db()
use(db)

import chcko.chcko.app

def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with chcko.chcko.db.db.dbclient.context():
            return wsgi_app(environ, start_response)
    return middleware
app = ndb_wsgi_middleware(chcko.chcko.app.app)
