# -*- coding: utf-8 -*-

import sys
import os
from traceback import print_exc

from chcko.chcko import bottle
from chcko.chcko.bottle import HTTPError
app = bottle.app()

from chcko.chcko.hlp import chcko_import
from chcko.chcko.languages import langnumkind
from chcko.chcko.db import db

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
    if pagename == 'null': #XXX: why does this null happen?
        raise ValueError(pagename)
    if pagename is None:# or pagename=='null':
        pagename = 'content'
    return lang,pagename

@bottle.hook('before_request')
def trailing_slash():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip('/')

ROOT = os.path.dirname(os.path.dirname(__file__))

@bottle.route('/favicon.ico')
def serve_favicon():
    return bottle.static_file(os.path.join('chcko','static','favicon.ico'), root=ROOT)

@bottle.route('/<ignoredir>/_images/<filename>')
def serve_image(ignoredir,filename):
    return bottle.static_file(os.path.join('_images',filename), root=ROOT)

@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(os.path.join('chcko','static',filename), root=ROOT)

from requests_oauthlib import OAuth2Session
from urllib.parse import urljoin
from chcko.chcko import auth
@bottle.route('/auth/<provider>')
def auth_login(provider):
    PROVIDER = provider.upper()
    client_id = os.environ[f'{PROVIDER}_CLIENT_ID']
    client_secret = os.environ[f'{PROVIDER}_CLIENT_SECRET']
    redirect_uri=urljoin(bottle.request.url, f'/auth/{provider}/callback')
    provider_auth = OAuth2Session(client_id
                          ,redirect_uri=redirect_uri
                          ,scope=auth.provider.client_kwargs['scope']
                          )
    authorize_url, state = provider_auth.authorization_url(
            auth.provider.authorize_url
            , **auth.provider.client_kwargs
            )
    redirect(authorize_url)
@bottle.route('/auth/<provider>/callback')
def auth_callback(provider):
    client_id = os.environ[f'{PROVIDER}_CLIENT_ID']
    provider_auth = OAuth2Session(client_id
                                  , token=token
                                  , auto_refresh_url=refresh_url
                                  , auto_refresh_kwargs=extra
                                  , token_updater=token_saver)
    r = provider_auth.get(protected_url)
    user_info = remote.profile(token=token)
    return handle_authorize(remote, token, user_info)


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
    bottle.request.lang = lang
    bottle.request.pagename = pagename
    db.set_user(bottle.request,bottle.response)
    errormsg = db.set_student(bottle.request,bottle.response)
    if errormsg is not None:
        bottle.redirect(f'/{lang}/{errormsg}')
    try:
        m = chcko_import('chcko.'+pagename)
        page = m.Page()
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

