"""
Contains entry point ``app`` for google cloud platform.
"""

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
