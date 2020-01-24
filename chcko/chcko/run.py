
def main():
    from chcko.chcko.db import use
    from chcko.chcko.sql import Sql
    db = Sql()
    with db.dbclient.context():
        db.init_db()
    use(db)
    import chcko.chcko.app
    import bottle
    bottle.run(app=chcko.chcko.app.app)

if __name__ == "__main__":
    main()
