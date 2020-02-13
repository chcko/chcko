
import sys
import os

def main(server='gunicorn'):
    thisdir = os.path.abspath('.')
    if not thisdir in sys.path:
        sys.path.insert(0,thisdir)
    from chcko.chcko.db import use
    from chcko.chcko.sql import Sql
    db = Sql()
    with db.dbclient.context():
        db.init_db()
    use(db)
    import chcko.chcko.app
    from chcko.chcko import bottle
    if server is None:
        bottle.run(app=chcko.chcko.app.app)
        return
    try:
        bottle.run(app=chcko.chcko.app.app, server=server)
    except:
        bottle.run(app=chcko.chcko.app.app)

if __name__ == "__main__":
    main()
