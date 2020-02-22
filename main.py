"""
Contains entry point ``app`` for google cloud platform.
"""

#####################################
# To run with dev_appserver.py
# ~/mine
# python2 `which dev_appserver.py` chcko
# https://stackoverflow.com/questions/54507222/localhost-how-to-get-credentials-to-connect-gae-python-3-app-and-datastore-emul
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
    # localhost
    from unittest import mock
    from google.cloud import datastore
    import google.auth.credentials
    os.environ["DATASTORE_DATASET"] = "chcko-262117"
    os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8081"
    os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8081/datastore"
    os.environ["DATASTORE_HOST"] = "http://localhost:8081"
    os.environ["DATASTORE_PROJECT_ID"] = "chcko-262117"
    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    dta = datastore.Client(project="chcko-262117", credentials=credentials)

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
