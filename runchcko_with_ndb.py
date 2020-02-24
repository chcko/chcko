#!/usr/bin/env python

if __name__ == '__main__':
    import conftest
    import os
    os.environ['CHCKOTESTING'] = "no"

    with conftest.emulator():

        import main

        config = {'bind': "127.0.0.1:8080"}
        print_serve = lambda: print('Serving at',config['bind'])

        try:
            from gunicorn.app.base import Application
            class GunicornApplication(Application):
                def init(self, parser, opts, args):
                    return config
                def load(self):
                    return main.app
            print_serve()
            GunicornApplication().run()

        except Exception as e:

            from wsgiref.simple_server import make_server
            host, port = config['bind'].split(':')
            server = make_server(host, int(port), main.app)
            try:
                print_serve()
                server.serve_forever()
            except KeyboardInterrupt:
                server.server_close()

