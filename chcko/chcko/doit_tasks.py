# -*- coding: utf-8 -*-
'''
doit utility::

Do this after having changed an RST file::

    $ cd chcko-x/chcko
    $ doit -kd. html

Do this after having changed the header (path, kind, level) in a html or rst file::

    $ cd chcko-x/chcko
    $ doit -kd. initdb
    $ doit -kd. clean #to clean again

Do this after any changes, especially in the main code::

    $ doit test
    $ doit cov

Do this to add new content, html or rst::

    $ cd chcko-x/chcko
    $ doit -kd. new
    $ doit -kd. rst

task_included is internal.

'''

import os
from subprocess import check_output
import sys
import re
import fnmatch
import shutil
import codecs
from itertools import count
from numpy import base_repr

import pytest

import chcko.chcko.languages as languages
import pprint

from doit.task import clean_targets

is_win = (sys.platform == 'win32')
PY3 = sys.version_info[0] == 3
def iteritems(d, **kw):
    return iter(getattr(d, "items" if PY3 else "iteritems")(**kw))

listdir = lambda x: sorted(os.listdir(x))

basedir = None
thisdir = None
sphinxbase = None
authorbase = None
author_id = None
authorbase = None
def set_base(dodofile):
    global basedir
    global thisdir
    global sphinxbase
    global author_id
    global authorbase
    # basedir = os.path.expanduser('~/mine/chcko-r')
    basedir = os.path.dirname(dodofile)
    author_id = basedir.rsplit('-',1)[-1]
    thisdir = os.getcwd()
    sphinxbase = os.path.join(basedir,'chcko')
    authorbase = os.path.join(basedir,'chcko',author_id)

problemids = lambda: list(x for x in listdir(authorbase)
    if not any(u in x for u in '._') and os.path.isdir(os.path.join(authorbase,x)))


def recursive_glob(pattern):
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return filter(lambda x: not any([x.find(w)>=0 for w in [
        'CHANGELOG.rst','README.rst','bottle','simpleauth','sympy']]), matches)

def task_included():
    '''tasks that find files (recursively) included by one rst file or tex file
    '''
    rstinclude = re.compile(r'\n\.\. (?:include|texfigure)::\s*(.*)')
    #[m.group(1) for m in rstinclude.finditer('\n\n.. texfigure:: test.tex\n')]
    texinput = re.compile(r'\n\\(?:input|include)\s*{([^}]*)}')
    #[m.group(1) for m in texinput.finditer('\n\n\\input{test}\n')]
    include_rexes = {'.rst':rstinclude,'.tex':texinput}
    def includes(filename,ext,rex):
        pathn,filen = os.path.split(filename)
        incs = []
        with open(filename) as f:
            for m in rex.finditer(f.read()):
                included = m.group(1)
                fn,ex = os.path.splitext(included)
                if not ex:#\input can go without '.tex'
                    included = fn+ext
                included = os.path.join(pathn,included)
                incs.append(included)
        return {'file_dep': incs,
                'calc_dep': ['included:includes:'+x for x in incs]
                }
    for ext, rex in iteritems(include_rexes):
        for fn in recursive_glob('*'+ext):
            yield {'name': 'includes:'+fn,
               'actions': [(includes,(fn,ext,rex))],
               'file_dep': [fn],
               }

def task_html():
    r'''Compile rst files in directory to html (body only) using Sphinx.

    ``conf.py`` uses ``page.html`` (containing {{body}}) as template. Both are in this directory.

    The rst file can have texfigure includes (or tikz or any other installed sphinxcontrib package)::

        .. texfigure:: diagram.tex
             :align: center

    The tex file can itself include other tex files (\input{othertexfile}).

    Images are moved to ``_images``.
    '''

    os.chdir(thisdir) # other task generators might have changed cwd

    sphinxbuild = ['sphinx-build']
    conf_py = ['-c',sphinxbase,'-Q']
    dfn = lambda n,v:['-D',n+'='+v]

    sphinxcmd = lambda srcpath,master,build: (sphinxbuild + conf_py +
            dfn('master_doc',master) +
            dfn('project',os.path.basename(srcpath)) +
            [srcpath,build])
    #sphinxcmd('srcpath','name','build')

    def move_images_if_any(build):
        try:
            imagepath = os.path.join(build, '_images')
            images = listdir(imagepath)
            imagedest = os.path.join(sphinxbase, '_images')
            if not os.path.exists(imagedest):
                os.makedirs(imagedest)
            for img in images:
                imgfile = os.path.join(imagepath,img)
                shutil.move(imgfile, os.path.join(imagedest,img))
        except OSError:
            pass
        return True

    sources = recursive_glob('*.rst')

    for src in sources:
        srcpath,srcname = os.path.split(src)
        name = os.path.splitext(srcname)[0]
        build = os.path.join(srcpath,'_build')
        tmptgt = os.path.join(build,name+'.html')
        # everything starting with _ is generated
        finaltgt = os.path.join(srcpath,'_'+name+'.html')
        yield {'name':finaltgt+'('+src+')',
            'actions':[ sphinxcmd(srcpath,name,build),
                          (move_images_if_any,[build]),
                          ['mv', tmptgt, finaltgt],
                          ['rm', '-rf', build]
                         ],
            'file_dep':[src],
            'calc_dep':['included:includes:'+src],
            'targets':[finaltgt],
            'clean':[clean_targets]}


### create new problem / content
nostartnum = re.compile('^\d+.*$')
def author_next():
    ids = problemids()
    idcount = count()
    for testid in idcount:
        next_id = base_repr(testid,36).lower()
        if nostartnum.match(next_id):
            continue
        if next_id not in ids:
            break
    return author_id, next_id

init_starter = '''
# # for a problem uncomment (non-problem texts need no code in __init__.py)
# from chcko.chcko.hlp import Struct
# # randomize numbers using e.g. sample and randrange
# import random
# def given():
#     g = Struct()
#     # fill g
#     return g
# def calc(g):
#     res = []
#     # fill res
#     return res
# # #remove if default norm_rounded works fine
# # def norm(answers):
# #     return norm_rounded(answers)
# # #remove if default equal_eq works fine
# # def equal(a, r):
# #     return equal_eq(a, r)
'''

lang_starter = '''
    %path = "path/goes/here"
    %kind = 0 #problems
    %level = 0 # in school years
    <!-- html -->

'''

def new_path():
    author_id, next_id = author_next()
    path = os.path.join(basedir,'chcko',author_id,next_id)
    os.makedirs(path)
    return path

def newproblem(init_starter=init_starter,lang_starter=lang_starter):
    try:
        path = new_path()
        with open(os.path.join(path,'__init__.py'),'a') as f:
            f.write(init_starter)
        with open(os.path.join(path,'en'+'.html'),'a') as f:
            f.write(lang_starter)
        return path
    except OSError:
        raise OSError('ID path exists.')

rst_starter = f'''.. raw:: html
{lang_starter}
'''

def newrst(rst_starter=rst_starter):
    try:
        path = new_path()
        with open(os.path.join(path,'__init__.py'),'a') as f:
            f.write(init_starter)
        with open(os.path.join(path,'en.rst'),'a') as f:
            f.write(rst_starter)
        return path
    except OSError:
        raise OSError('ID path exists.')

def task_new():
    return {
            'actions':[newproblem],
           }

def task_rst():
    return {
            'actions':[newrst],
           }


def task_initdb():

    def make_initdb():
        available_langs = set([])
        inits = ['# -*- coding: utf-8 -*-',
                 '# generate via ``doit -kd. initdb``',
                 'def populate_index(index_add):']
        ids = problemids()
        for anid in ids:
            def langcode(x):
                lng_ext = x.split('.')
                if len(lng_ext) == 2:
                    lng,ext = lng_ext
                    return ext == 'html' and lng.strip('_')
            problemdir = os.path.join(authorbase,anid)
            langfiles = [fl for fl in listdir(problemdir)
                    if langcode(fl) in languages.languages]
            for langfile in langfiles:
                full = os.path.join(problemdir,langfile)
                with open(full,'rb') as ff:
                    src = codecs.decode(ff.read(),'utf-8')
                defines = []
                for ln in src.splitlines():
                    lnstr = ln.strip()
                    if lnstr:
                        if not lnstr.startswith('%'):
                            break
                        lnstr1 = lnstr[1:]
                        defines.append(lnstr1)
                        if lnstr1.strip().startswith('level'):
                            break # level must be last define
                deftext = u'\n'.join(defines)
                lang = langcode(langfile)
                available_langs.add(lang)
                defs = {'kinda':languages.langkindnum[lang]}
                try:
                    exec(deftext, defs)
                except KeyError:
                    print(full)
                    raise
                inits.append('    index_add("{0}", "{1}", "{2}", "{3}",\n        "{4}")'.format(
                    author_id+'.'+anid
                    ,lang
                    ,defs['kind']
                    ,defs['level']
                    ,defs['path']))
            initdb = os.path.join(authorbase,'initdb.py')
            with open(initdb, 'w') as f:
                f.write('\n'.join(inits))
                f.write('\n\n')
                f.write('available_langs = ')
                f.write(pprint.pformat(available_langs,width=1))
                f.write('\n')

        # assert that languages does not need more localization
        langdicts = [(k,o) for k,o in iteritems(languages.__dict__)
                if not k.startswith('__') and isinstance(o,dict)]
        for k,o in langdicts:
            extendlangs = available_langs - set(o.keys())
            assert not extendlangs, k + ' in languages.py needs ' + ','.join(extendlangs)

    return {'actions':[make_initdb]}

