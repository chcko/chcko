# -*- coding: utf-8 -*-

import sys
import os
from traceback import print_exc

from chcko.chcko import bottle
from chcko.chcko.bottle import HTTPError
app = bottle.app()

from chcko.chcko.util import user_required
from chcko.chcko.hlp import chcko_import
from chcko.chcko.languages import langnumkind
from chcko.chcko.db import db
from functools import partial

def lang_pagename(lang=None,pagename=None):
    if lang is None:
        lang = db.get_cookie('chcko_cookie_lang')
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
    if pagename == 'null': #XXX: why does this null happen?
        raise ValueError(pagename)
    if pagename is None:# or pagename=='null':
        pagename = 'content'
    return lang,pagename

@bottle.hook('before_request')
def trailing_slash():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip('/')

ROOT = os.path.dirname(os.path.dirname(__file__))

#for google verification
@bottle.route('/<filename>.html')
def statichtml(filename):
    return bottle.static_file(filename+'.html', root=ROOT)

@bottle.route('/favicon.ico')
def serve_favicon():
    return bottle.static_file(os.path.join('chcko','static','favicon.ico'), root=ROOT)

@bottle.route('/<ignoredir>/_images/<filename>')
def serve_image(ignoredir,filename):
    return bottle.static_file(os.path.join('_images',filename), root=ROOT)

@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(os.path.join('chcko','static',filename), root=ROOT)

#social
try:
    from social_core.exceptions import SocialAuthBaseException
    from social_core.actions import do_auth, do_complete
    from chcko.chcko.auth import make_backend_obj, social_login_name
    @bottle.route('/auth/<provider>', method=('GET', 'POST'))
    @make_backend_obj()
    def auth_login(backend):
        try:
            backend.strategy.session_pop(backend.name + '_state')
            do_auth(backend)
        except SocialAuthBaseException:
            bottle.redirect('/')
    @bottle.route('/auth/<provider>/callback', method=('GET', 'POST'))
    @make_backend_obj()
    def auth_callback(backend):
        try:
            user = do_complete(backend, login=None)
        except SocialAuthBaseException:
            pass
        db.set_cookie('chcko_cookie_usertoken',bottle.request.user.token)
        bottle.redirect('/')
    #this is called via social_core
    def social_user(backend, uid, user=None, *args, **kwargs):
        sln = social_login_name(backend.__class__)
        info = kwargs['details']
        fullname = f'{info["fullname"]} ({sln})'
        jwt = kwargs['response']
        try:
            lang = jwt['locale']
        except:
            lang = 'en'
        email = info['email']
        verified = True
        if not email:
            email = fullname
            verified = False
        token = db.token_create(email)
        user, token = db.user_login(email,fullname=fullname,token=token,lang=lang,verified=verified)
        bottle.request.user = user
        #statisfy social_core:
        class AttributeDict(dict): 
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        kwargs['user'] = AttributeDict()
        kwargs['social'] = user
        kwargs['is_new'] = None
        kwargs['user'].social = user
        return kwargs
except:
    pass

@bottle.route('/',method=['GET','POST'])
def nopath():
    return fullpath(None,None)

@bottle.route('/<lang>',method=['GET','POST'])
def langonly(lang):
    return fullpath(lang,None)

@bottle.route('/<lang>/logout')
def logout(lang):
    t = db.get_cookie('chcko_cookie_usertoken')
    if t:
        db.token_delete(t)
        bottle.response.delete_cookie('chcko_cookie_usertoken')
    bottle.redirect(f'/{lang}/content')

@bottle.route('/<lang>/<pagename>',method=['GET','POST'])
def fullpath(lang,pagename):
    try:
        lang,pagename = lang_pagename(lang,pagename)
    except ValueError:
        return ""
    db.set_cookie('chcko_cookie_lang',lang)
    bottle.request.lang = lang
    bottle.request.pagename = pagename
    db.user_by_cookie()
    db.student_by()
    try:
        mod = chcko_import('chcko.'+pagename)
        page = mod.Page(mod)
        if bottle.request.route.method == 'GET':
            respns = page.get_response()
        else:
            respns = page.post_response()
        return respns
    except (ImportError, AttributeError, IOError, NameError) as e:
        print_exc()
        bottle.redirect(f'/{lang}')
    except:
        print_exc()
        raise

