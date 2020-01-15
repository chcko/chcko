# -*- coding: utf-8 -*-

import sys
import os
import os.path
from traceback import print_exc

from chcko import bottle
from chcko.bottle import HTTPError
app = bottle.app()

ROOT = os.path.dirname(__file__)
def python_path():
    prjroot = os.path.dirname(ROOT)
    if prjroot not in sys.path:
        sys.path.insert(0, prjroot)
python_path()

from chcko.hlp import import_module
from chcko.languages import langnumkind
from chcko.db import db

def lang_pagename(lang=None,pagename=None):
    if lang is None:
        lang = bottle.request.get_cookie('chckolang')
    if lang not in langnumkind:
        if pagename == None:
            pagename = lang
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
    if pagename is None:
        pagename = bottle.request.get_cookie('chckopage')
    if pagename == 'null':
        raise ValueError(pagename)
    if pagename is None or pagename=='null':
        pagename = 'content'
    return lang,pagename

@bottle.hook('before_request')
def trailing_slash():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip('/')

@bottle.route('/favicon.ico')
def serve_favicon():
    return bottle.static_file(os.path.join('static','favicon.ico'), root=ROOT)

#TODO: the images should rather stay in their contextual folder
@bottle.route('/<ignoredir>/_images/<filename>')
def serve_image(ignoredir,filename):
    return bottle.static_file(os.path.join('_images',filename), root=ROOT)

@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(os.path.join('static',filename), root=ROOT)

@bottle.route('/',method=['GET','POST'])
def nopath():
    return fullpath(None,None)

@bottle.route('/<lang>',method=['GET','POST'])
def langonly(lang):
    return fullpath(lang,None)

@bottle.route('/<lang>/logout')
def logout(lang):
    t = bottle.request.get_cookie('chckousertoken')
    if t:
        db.token_delete(t)
        bottle.response.delete_cookie('chckousertoken')
    bottle.redirect(f'/{lang}/content')

@bottle.route('/<lang>/<pagename>',method=['GET','POST'])
def fullpath(lang,pagename):
    try:
        lang,pagename = lang_pagename(lang,pagename)
    except ValueError:
        return ""
    db.set_cookie(bottle.response,'chckolang',lang)
    db.set_cookie(bottle.response,'chckopage',pagename)
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

