'''
This is the main application file.

The whole application has only a class derived from webapp2.RequestHandler.
After a little analysis of the query,
it forwards to classes derived form PageBase in util.py.
'''

import sys
import os
import os.path
import logging

# TODO
# from bottle import *
# #bottle has an app object
# bottle_app = app


# TODO check outdated
# execute the following in vim py to use google appengine in vim
#>> from chcko.conftest import gaetestbed
#>> class requestdummy:
#>>     def addfinalizer(self,fin):
#>>         self.fin=fin
#>> finrequest = requestdummy()
#>> finalize = gaetestbed(finrequest)
# finalize()

def python_path():
    this_file = os.path.abspath(__file__)
    local_dir = os.path.join(os.path.dirname(this_file), "..")
    local_dir = os.path.normpath(local_dir)
    if local_dir not in sys.path:
        sys.path.insert(0, local_dir)

python_path()

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name=name)



#auth
#https://raw.githubusercontent.com/Refinitiv/bottle-oauthlib/master/tests/examples/quickstart.py
#auth


import webapp2
from webapp2_extras import sessions

from chcko.hlp import import_module, PAGES, is_standard_server
from chcko.util import AuthUser
from chcko.model import stored_secret, set_student, db

# this will fill Index
# initdb is generate via `doit -k initdb`
from chcko.initdb import available_langs
from chcko.languages import langnumkind

from simpleauth import SimpleAuthHandler

class PageHandler(webapp2.RequestHandler, SimpleAuthHandler, AuthUser):

    '''http://chcko.appspot.com/<lang>/[<pagename>]?<query_string>

    pagename defaults to 'content'

    The handler class derived from PageBase
    is in a python package module of name "pagename",
    of which it calls ``get_response()`` or ``post_response()``.

    '''

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        # set_student will modify the session
        # if self.session_store.get_session().new:
        # self.session.update({})#modifies session to re-put/re-send
        try:
            webapp2.RequestHandler.dispatch(self)
            try:
                self.session['lang'] = self.request.lang
            except AttributeError: #for auth
                pass
        finally:
            self.session_store.save_sessions(self.response)

    # Enable optional OAuth 2.0 CSRF guard
    OAUTH2_CSRF_STATE = True  # needs self.session
    ATTRS = {
        'facebook': {
            'id': lambda id: (
                'avatar_url',
                'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
            'name': 'name',
            'link': 'link'},
        'google': {
            'picture': 'avatar_url',
            'name': 'name',
            'profile': 'link'},
        'twitter': {
            'profile_image_url': 'avatar_url',
            'screen_name': 'name',
            'link': 'link'},
        'linkedin2': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'},
        'foursquare': {
            'photo': lambda photo: (
                'avatar_url',
                photo.get('prefix') +
                '100x100' +
                photo.get('suffix')),
            'firstName': 'firstName',
            'lastName': 'lastName',
            'contact': lambda contact: (
                'email',
                contact.get('email')),
            'id': lambda id: (
                'link',
                'http://foursquare.com/user/{0}'.format(id))},
        'openid': {
            'id': lambda id: (
                'avatar_url',
                '/img/missing-avatar.png'),
            'nickname': 'name',
            'email': 'link'}}
    #
    # secrets need to be uploaded manually
    # http://stackoverflow.com/questions/1782906/how-do-i-activate-the-interactive-console-on-app-engine
    # https://developers.google.com/appengine/docs/adminconsole/
    # https://developers.google.com/appengine/articles/remote_api
    # remote_api_shell.py #http://chcko.appspot.com/admin/interactive is off
    #$remote_api_shell.py -s chcko.appspot.com
    #>> import chcko.model as mdl
    #>> mdl.Secret.query().fetch()
    #>> mdl.Secret.get_or_insert("test", secret = "test secret")
    #
    # client ids need to be registed:
    # http://code.google.com/apis/console
    # https://developers.facebook.com/apps
    # https://www.linkedin.com/secure/developer
    # https://dev.twitter.com/apps
    # openid no registration needed, but Authentication Type = Federated Login at
    #  https://appengine.google.com/settings?app_id=s~chcko
    SECRETS = {p: (stored_secret(p + 'chckoid'), stored_secret(p))
               for p in ATTRS.keys()}
    SCOPES = {
        # OAuth 2.0 providers
        'google': 'https://www.googleapis.com/auth/userinfo.profile',
        'linkedin2': 'r_basicprofile',
        'facebook': 'user_about_me',
        'foursquare': 'authorization_code',
        # OAuth 1.0 providers don't have scopes
        'twitter': '',
        'linkedin': '',
        # openid doesn't need any key/secret
    }

    def _callback_uri_for(self, provider):
        return self.uri_for('callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        return tuple(
            filter(None, list(self.SECRETS[provider]) + [self.SCOPES[provider]]))

    def _on_signin(self, data, auth_info, provider):
        auth_id = '%s:%s' % (provider, data['id'])
        user = self.user_model.get_by_auth_id(auth_id)
        _attrs = {}
        for k, v in self.ATTRS[provider].iteritems():
            attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
            _attrs.setdefault(*attr)
        if user:
            user.populate(**_attrs)
            user.put()
            self.auth.set_session(
                self.auth.store.user_to_dict(user))
        else:
            if self.logged_in:
                u = self.user
                u.populate(**_attrs)
                success, info = u.add_auth_id(auth_id)  # this will put()
                if not success:
                    logging.warning('Update existing user failed')
            else:
                ok, user = self.auth.store.user_model.create_user(
                    auth_id, **_attrs)
                if ok:
                    self.auth.set_session(self.auth.store.user_to_dict(user))
        try:
            lang = self.session['lang']
        except KeyError:
            lang = 'en'
        self.redirect(self.uri_for('entry_lang', lang=lang))

    def logout(self, lang):
        self.auth.unset_session()
        self.redirect(self.uri_for('entry_lang', lang=lang))

    def arguments_ok(self, kwargs):
        #kwargs = {}
        self.request.lang = kwargs.get('lang', None)
        self.request.pagename = kwargs.get('pagename', None)

        if not self.request.lang or not self.request.lang in langnumkind:
            try:
                lng = self.session['lang']
            except KeyError:
                langs = self.request.headers.get('Accept-Language')
                if langs:
                    langs = langs.split(',')
                else:
                    langs = []
                #langs = ['en-US', 'en;q=0.8']
                accepted = set([x.split(';q=')[0].split('-')[0] for x in langs])
                #accepted = set(['en'])
                candidates = accepted & available_langs
                if candidates:
                    lng = list(candidates)[0]
                else:
                    lng = 'en'
            if self.request.lang and not self.request.lang in langnumkind:
                self.request.pagename = self.request.lang
            self.request.lang = lng
        if not self.request.pagename:
            self.request.pagename = 'content'
        if self.request.pagename not in PAGES:
            self.redirect(self.uri_for('entry_lang', lang=self.request.lang))
            return
        studentres = set_student(self.request, self.user, self.session)
        if isinstance(studentres, str):
            self.redirect(studentres)
            return
        return True

    def forward(self, kwargs, toforward):
        if self.arguments_ok(kwargs):
            try:
                self.request.modulename = self.request.pagename
                m = import_module(self.request.modulename)
                page = m.Page(self.request)
                self.response.write(toforward(page))
            except (ImportError, AttributeError, IOError, NameError) as e:
                if not is_standard_server:
                    raise
                self.redirect(
                    self.uri_for(
                        'entry_lang',
                        lang=self.request.lang))

    def get(self, **kwargs):
        self.forward(kwargs, lambda page: page.get_response())

    def post(self, **kwargs):
        self.forward(kwargs, lambda page: page.post_response())

# access via self.app.config.get('foo')
app_config = {
    'webapp2_extras.sessions': {
        'cookie_name': 'chckosessionkey',
        'secret_key': stored_secret('session_secret')
    },
    'webapp2_extras.auth': {
        'cookie_name': None,  # use the one from session config and not 'auth'
        'user_model': 'chcko.model.User',
        'user_attributes': ['name']
    }
}


def _error(request, response, exception, status):
    logging.exception(exception)
    response.write(
        'Error ' +
        str(status) +
        ' (' +
        str(exception.message) +
        ')')
    response.set_status(status)


def make_app(debug_=not is_standard_server):
    app_ = webapp2.WSGIApplication([
        webapp2.Route('', handler=PageHandler, name='entry'),
        webapp2.Route('/', handler=PageHandler, name='entry_'),
        webapp2.Route('/<lang:[^/]+>', handler=PageHandler, name='entry_lang'),
        webapp2.Route('/<lang:[^/]+>/', handler=PageHandler, name='entry_lang_'),
        webapp2.Route('/<lang:[^/]+>/logout',
            handler='chcko.app.PageHandler:logout', name='logout'),
        webapp2.Route('/auth/<provider>',
            handler='chcko.app.PageHandler:_simple_auth', name='authlogin'),
        #no lang for auth callback, therefore lang is also in the session
        webapp2.Route('/auth/<provider>/callback',
            handler='chcko.app.PageHandler:_auth_callback', name='callback'),
        webapp2.Route('/<lang:[^/]+>/<pagename:[^?]+>', handler=PageHandler, name='page'),
    ], config=app_config, debug=debug_)
    app_.error_handlers[400] = lambda q, a, e: _error(q, a, e, 400)
    app_.error_handlers[404] = lambda q, a, e: _error(q, a, e, 404)
    app_.error_handlers[500] = lambda q, a, e: _error(q, a, e, 500)
    return app_

webapp = make_app()

def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with db.context():
            return wsgi_app(environ, start_response)
    return middleware

app = ndb_wsgi_middleware(webapp)

# TODO, when using bottle
# app = ndb_wsgi_middleware(bottle_app)
# if __name__ == "__main__":
#     run(host='localhost', port=8080)
# 
