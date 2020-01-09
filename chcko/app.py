# -*- coding: utf-8 -*-

import sys
import os
import os.path
from traceback import print_exc

from chcko import bottle
from chcko.bottle import HTTPError
app = bottle.app()

def python_path():
    d = os.path.dirname
    local_dir = d(d(__file__))
    if local_dir not in sys.path:
        sys.path.insert(0, local_dir)
python_path()

from chcko.hlp import import_module
from chcko.languages import langnumkind
from chcko.db import db

def find_lang():
    lang = bottle.request.get_cookie('chckolang')
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

def find_pagename(lang):
    pagename = bottle.request.get_cookie('chckolastpage')
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
def nopath():
    lang = find_lang()
    lang,pagename = find_pagename(lang)
    return fullpath(lang,pagename)

@bottle.route('/<lang>',method=['GET','POST'])
def langonly(lang):
    lang,pagename = find_pagename(lang)
    return fullpath(lang,pagename)

@bottle.route('/<lang>/logout')
def logout(lang):
    t = bottle.request.get_cookie('chckousertoken')
    if t:
        db.token_delete(t)
        bottle.response.delete_cookie('chckousertoken')
    bottle.redirect(f'/{lang}/content')

@bottle.route('/<lang>/<pagename>',method=['GET','POST'])
def fullpath(lang,pagename):
    bottle.request.lang = lang
    bottle.request.pagename = pagename
    db.set_user(bottle.request,bottle.response)
    errormsg = db.set_student(bottle.request,bottle.response)
    if errormsg is not None:
        bottle.redirect(f'/{lang}/{errormsg}')
    try:
        m = import_module(pagename)
        page = m.Page()
        if bottle.request.route.method == 'GET':
            respns = page.get_response()
        else:
            respns = page.post_response()
        print([x.oks for x in db.allof(db.query(db.Problem)) if None in x.oks])#R#
        return respns
    except (ImportError, AttributeError, IOError, NameError) as e:
        print_exc()
        #TODO: logging
        bottle.redirect(f'/{lang}')

@bottle.route('/<lang>/auth/<provider>')
def auth(provider):
    pass

@bottle.route('/<lang>/auth/<provider>/callback')
def auth_callback(provider):
    pass

if __name__ == "__main__":
    run(host='localhost', port=8000)
