"""
Contains entry point ``app`` for google cloud platform.
"""

from chcko.db import use
from chcko.ndb import Ndb
use(Ndb())
import chcko.app

def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with chcko.db.db.dbclient.context():
            return wsgi_app(environ, start_response)
    return middleware
app = ndb_wsgi_middleware(chcko.app.app)
