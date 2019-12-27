# -*- coding: utf-8 -*-

import sys
import os
import os.path
import logging

from chcko import bottle
import bottle_session as bs
app = bottle.app()
try:
    app.install(bs.SessionPlugin(cookie_name='chcko',cookie_lifetime=bs.MAX_TTL))
except:
    pass

def python_path():
    d = os.path.dirname
    local_dir = d(d(__file__))
    if local_dir not in sys.path:
        sys.path.insert(0, local_dir)
python_path()

from chcko.hlp import import_module, PAGES, is_standard_server, mklookup
from chcko.languages import langnumkind
from chcko.db import db

from oauthlib import oauth2
class OAuth2_ResourceValidator(oauth2.RequestValidator):
    def validate_bearer_token(self, token, subject, request):
        if not token:
            return False
        try:
            request.user, _ = db.user_timestamp_by_token(token, subject)
        except:
            return False
        return True
from bottle_oauthlib.oauth2 import BottleOAuth2
app.auth = BottleOAuth2(app)
app.auth.initialize(
    oauth2.ResourceEndpoint(
        default_token='Bearer',
        token_types={
            'Bearer': oauth2.BearerToken(OAuth2_ResourceValidator())
        }
    )
)

def find_lang(session):
    lang = None
    try:
        lang = session['lang']
    except:
        pass
    if lang is None:
        langs = bottle.request.headers.get('Accept-Language')
        if langs:
            langs = langs.split(',')
        else:
            langs = []
        #langs = ['en-US', 'en;q=0.8']
        accepted = set([x.split(';q=')[0].split('-')[0] for x in langs])
        #accepted = set(['en'])
        candidates = accepted & db.available_langs
        if candidates:
            lang = list(candidates)[0]
        else:
            lang = 'en'
    return lang

def find_pagename(session,lang):
    pagename = None
    try:
        pagename = session['pagename']
    except:
        pass
    if pagename is None:
        if lang not in langnumkind:
            pagename = lang
        else:
            pagename = 'content'
    if pagename not in PAGES:
        pagename = 'content'
    return pagename

@bottle.hook('before_request')
def trailing_slash():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip('/')

@bottle.route('/')
def entry(session):
    lang = find_lang(session)
    pagename = find_pagename(session,lang)
    bottle.redirect('/'+lang+'/'+pagename)

@bottle.route('/lang')
def lang(session,lang):
    pagename = find_pagename(session,lang)
    bottle.redirect('/'+lang+'/'+pagename)

@bottle.route('/<lang>/<pagename>',method=['get','post'])
def pagename(session,lang,pagename):
    bottle.request.session = session
    bottle.request.lang = lang
    bottle.request.pagename = pagename
    db.set_user(bottle.request)
    errormsg = db.set_student(bottle.request)
    if errormsg is not None:
        bottle.redirect('/'+lang+'/'+errormsg)
    try:
        m = import_module(pagename)
        page = m.Page(bottle.request)
        if bottle.request.route.method == 'get':
            return page.get_response()
        else:
            return page.post_response()
    except (ImportError, AttributeError, IOError, NameError) as e:
        if not is_standard_server:
            raise
        bottle.redirect('/'+lang)

@bottle.route('/<lang>/logout')
def logout(session):
    session.destroy()
    bottle.redirect('/lang')

@bottle.route('/<lang>/auth/<provider>')
def auth(session,provider):
    pass

@bottle.route('/<lang>/auth/<provider>/callback')
def auth_callback(session,provider):
    pass

if __name__ == "__main__":
    run(host='localhost', port=8000)
