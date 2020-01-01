# -*- coding: utf-8 -*-

import sys
import os
import os.path

from chcko import bottle
from chcko.bottle import HTTPError
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

from chcko.hlp import import_module
from chcko.languages import langnumkind
from chcko.db import db

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
            langs = ['en-US', 'en;q=0.8', 'de']
        accepted = set([x.split(';q=')[0].split('-')[0] for x in langs])
        candidates = accepted & db.available_langs
        if candidates:
            if 'en' in candidates:
                lang = 'en'
            else:
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
            lang = 'en'
        else:
            pagename = 'content'
    return lang,pagename

@bottle.hook('before_request')
def trailing_slash():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip('/')

@bottle.route('/',method=['GET','POST'])
def nopath(session):
    lang = find_lang(session)
    lang,pagename = find_pagename(session,lang)
    return fullpath(session,lang,pagename)

@bottle.route('/<lang>',method=['GET','POST'])
def langonly(session,lang):
    lang,pagename = find_pagename(session,lang)
    return fullpath(session,lang,pagename)

@bottle.route('/<lang>/<pagename>',method=['GET','POST'])
def fullpath(session,lang,pagename):
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
        if bottle.request.route.method == 'GET':
            return page.get_response()
        else:
            return page.post_response()
    except (ImportError, AttributeError, IOError, NameError) as e:
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
