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
from chcko.model import stored_secret, set_student

# this will fill Index
# initdb is generate via `doit -k initdb`
from chcko.initdb import available_langs
from chcko.languages import langnumkind

#A: from chcko.util import AuthUser
#A: from chcko.simpleauth import SimpleAuthHandler

class PageHandler(webapp2.RequestHandler):#A:, SimpleAuthHandler, AuthUser):

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
    #A: #
    #A: # secrets need to be uploaded manually
    #A: # http://stackoverflow.com/questions/1782906/how-do-i-activate-the-interactive-console-on-app-engine
    #A: # https://developers.google.com/appengine/docs/adminconsole/
    #A: # https://developers.google.com/appengine/articles/remote_api
    #A: # remote_api_shell.py #http://chcko.appspot.com/admin/interactive is off
    #A: #$remote_api_shell.py -s chcko.appspot.com
    #A: #>> import chcko.model as mdl
    #A: #>> mdl.Secret.query().fetch()
    #A: #>> mdl.Secret.get_or_insert("test", secret = "test secret")
    #A: #
    #A: # client ids need to be registed:
    #A: # http://code.google.com/apis/console
    #A: # https://developers.facebook.com/apps
    #A: # https://www.linkedin.com/secure/developer
    #A: # https://dev.twitter.com/apps
    #A: # openid no registration needed, but Authentication Type = Federated Login at
    #A: #  https://appengine.google.com/settings?app_id=s~chcko
    #A: SECRETS = {p: (stored_secret(p + 'chckoid'), stored_secret(p))
    #A:            for p in ATTRS.keys()}
    #A: SCOPES = {
    #A:     # OAuth 2.0 providers
    #A:     'google': 'https://www.googleapis.com/auth/userinfo.profile',
    #A:     'linkedin2': 'r_basicprofile',
    #A:     'facebook': 'user_about_me',
    #A:     'foursquare': 'authorization_code',
    #A:     # OAuth 1.0 providers don't have scopes
    #A:     'twitter': '',
    #A:     'linkedin': '',
    #A:     # openid doesn't need any key/secret
    #A:}

    #A:def _callback_uri_for(self, provider):
    #A:    return self.uri_for('callback', provider=provider, _full=True)

    #A:def _get_consumer_info_for(self, provider):
    #A:    return tuple(
    #A:        filter(None, list(self.SECRETS[provider]) + [self.SCOPES[provider]]))

    #A: def _on_signin(self, data, auth_info, provider):
    #A:     auth_id = '%s:%s' % (provider, data['id'])
    #A:     user = self.user_model.get_by_auth_id(auth_id)
    #A:     _attrs = {}
    #A:     for k, v in self.ATTRS[provider].iteritems():
    #A:         attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
    #A:         _attrs.setdefault(*attr)
    #A:     if user:
    #A:         user.populate(**_attrs)
    #A:         user.put()
    #A:         self.auth.set_session(
    #A:             self.auth.store.user_to_dict(user))
    #A:     else:
    #A:         if self.logged_in:
    #A:             u = self.user
    #A:             u.populate(**_attrs)
    #A:             success, info = u.add_auth_id(auth_id)  # this will put()
    #A:             if not success:
    #A:                 logging.warning('Update existing user failed')
    #A:         else:
    #A:             ok, user = self.auth.store.user_model.create_user(
    #A:                 auth_id, **_attrs)
    #A:             if ok:
    #A:                 self.auth.set_session(self.auth.store.user_to_dict(user))
    #A:     try:
    #A:         lang = self.session['lang']
    #A:     except KeyError:
    #A:         lang = 'en'
    #A:     self.redirect(self.uri_for('entry_lang', lang=lang))
    #A:
    #A: def logout(self, lang):
    #A:     self.auth.unset_session()
    #A:     self.redirect(self.uri_for('entry_lang', lang=lang))

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
app_config = {}
#A: app_config = {
#A:     'webapp2_extras.sessions': {
#A:         'cookie_name': 'chckosessionkey',
#A:         'secret_key': stored_secret('session_secret')
#A:     },
#A:     'webapp2_extras.auth': {
#A:         'cookie_name': None,  # use the one from session config and not 'auth'
#A:         'user_model': 'chcko.model.User',
#A:         'user_attributes': ['name']
#A:     }
#A: }


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
        #A:webapp2.Route('/<lang:[^/]+>/logout', handler='chcko.app.PageHandler:logout', name='logout'),
        #A:webapp2.Route('/auth/<provider>',handler='chcko.app.PageHandler:_simple_auth', name='authlogin'),
        #no lang for auth callback, therefore lang is also in the session
        #A:webapp2.Route('/auth/<provider>/callback',handler='chcko.app.PageHandler:_auth_callback', name='callback'),
        webapp2.Route('/<lang:[^/]+>/<pagename:[^?]+>', handler=PageHandler, name='page'),
    ], config=app_config, debug=debug_)
    app_.error_handlers[400] = lambda q, a, e: _error(q, a, e, 400)
    app_.error_handlers[404] = lambda q, a, e: _error(q, a, e, 404)
    app_.error_handlers[500] = lambda q, a, e: _error(q, a, e, 500)
    return app_

app = make_app()

# TODO, when using bottle
# if __name__ == "__main__":
#     run(host='localhost', port=8080)
