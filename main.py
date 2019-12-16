import chcko.app
from chcko.model import db
def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with db.context():
            return wsgi_app(environ, start_response)
    return middleware
app = ndb_wsgi_middleware(chcko.app.app)
