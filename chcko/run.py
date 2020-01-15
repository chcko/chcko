
def main():
    from chcko.db import use
    from chcko.sql import Sql
    db = Sql()
    with db.dbclient.context():
        db.init_db()
    use(db)
    import chcko.app
    import bottle
    bottle.run(app=chcko.app.app)

if __name__ == "__main__":
    main()
