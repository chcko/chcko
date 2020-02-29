import sys
import os

def main(server='gunicorn'):
    from chcko.chcko.db import use
    from chcko.chcko.sql import Sql
    db = Sql()
    with db.dbclient.context():
        db.init_db()
    use(db)
    import chcko.chcko.app
    from chcko.chcko import bottle
    try:
        chcko_port = os.environ['CHCKOPORT']
    except:
        chcko_port = 8080
    if server is None:
        bottle.run(app=chcko.chcko.app.app, port=chcko_port)
        return
    try:
        bottle.run(app=chcko.chcko.app.app, server=server, port=chcko_port)
    except:
        bottle.run(app=chcko.chcko.app.app, port=chcko_port)

if __name__ == "__main__":
    main()
