import sys
import os
import argparse

def run_server(server='gunicorn'):
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

def init_content(init):
    print("init_content not implemented")

def main(**args):
    if not args:
        parser = argparse.ArgumentParser(
            description =
            '''runs chcko server, if no parameters, else see parameter list.'''
        )
        parser.add_argument(
            '-i',
            '--init',
            action='store',
            help='''initialize a content package''')
        parser.add_argument(
            '-s',
            '--server',
            action='store',
            help='''run chcko server (default is gunicorn)''')
        #args={'server':'gunicorn'}
        args = list(filter(lambda x:print(x), parser.parse_args(args).__dict__.items()))
    if not args or not args['server']:
        args['server'] = 'gunicorn'
    if 'server' in args:
        run_server(args.pop('server'))
    if 'init' in args:
        init = args.pop('init')
        if init:
            init_content(init)

if __name__ == '__main__':
    main()
    os._exit(0)

