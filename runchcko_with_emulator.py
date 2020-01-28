#!/usr/bin/env python

if __name__ == '__main__':
    import conftest
    with conftest.emulator():

        import main
        from gunicorn.app.base import Application
        config = {'bind': "127.0.0.1:8080"}
        class GunicornApplication(Application):
            def init(self, parser, opts, args):
                return config
            def load(self):
                return main.app

        print('Serving at',config['bind'])
        GunicornApplication().run()
