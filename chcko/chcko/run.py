import sys
import os
import argparse
from txdir import to_tree
from subprocess import check_output

cwd = os.getcwd()
if os.path.split(cwd)[-1].startswith('chcko-'):
    if cwd not in sys.path:
        sys.path.insert(0,cwd)

def run_server(server='gunicorn'):
    from chcko.chcko.db import use
    from chcko.chcko.sql import Sql
    db = Sql()
    with db.dbclient.context():
        db.init_db()
    use(db)
    import chcko.chcko.app
    from chcko.chcko import bottle
    try:
        chcko_port = os.environ['CHCKOPORT']
    except:
        chcko_port = 8080
    if server is None:
        bottle.run(app=chcko.chcko.app.app, port=chcko_port)
        return
    try:
        bottle.run(app=chcko.chcko.app.app, server=server, port=chcko_port)
    except:
        bottle.run(app=chcko.chcko.app.app, port=chcko_port)

#uses << >> for { and }
txdirstr = r"""
chcko-{author_id}/MANIFEST.in
    include *.html
    graft chcko
    global-exclude __pycache__
    global-exclude *.py[co]
    global-exclude *.log
    global-exclude *.db
chcko-{author_id}/Makefile
    .PHONY: check render dist up

    check:
    	restview --long-description --strict

    render:
    	cd chcko/{author_id}
    	doit -kd. html
    	doit -kd. initdb

    dist:
    	sudo python setup.py bdist_wheel

    up:
    	twine upload dist/`ls dist -rt | tail -1`
chcko-{author_id}/README.rst
    chko-{author_id}
    ================

    TODO
chcko-{author_id}/dodo.py
    import sys
    import os
    chckouninstalled = os.path.normpath(os.path.join(os.path.dirname(__file__),'..','chcko'))
    if os.path.exists(chckouninstalled):
        sys.path.insert(0,chckouninstalled)
    from chcko.chcko import doit_tasks
    doit_tasks.set_base(__file__)
    task_included = doit_tasks.task_included
    task_html = doit_tasks.task_html
    task_initdb = doit_tasks.task_initdb
    task_new = doit_tasks.task_new
    task_rst = doit_tasks.task_rst
chcko-{author_id}/authors.yaml
    - author_id:      {author_id}
      gitname:        {author_name}
      gitemail:       {author_email}
      default_lang:   {author_lang}
      translate_to:   [{author_lang}]
      translate_from: []
chcko-{author_id}/nextids.yaml
    -
      {author_id}:  "b"
chcko-{author_id}/.gitignore
    .doit*
    **/_*
    !**/__*
    README.html
    *.rest
    WEB-INF/
    env.yaml
    __pycache__/
    *.py[cod]
    build/
    dist/
    *.egg*
chcko-{author_id}/chcko/page.html
    {{body}}
chcko-{author_id}/chcko/conf.py
    extensions = [
        'chcko.chcko.inl',
        'sphinx.ext.mathjax',
        'sphinxcontrib.tikz',
        'sphinxcontrib.texfigure']
    import os
    templates_path = [os.path.dirname(__file__)]
    del os
    source_suffix = '.rst'
    source_encoding = 'utf-8'
    default_role = 'math'
    pygments_style = 'sphinx'
    tikz_proc_suite = 'ImageMagick'
    tikz_tikzlibraries = 'arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks'
    latex_elements = dict(
        preamble='''\\usepackage<<amsfonts>>\\usepackage<<amssymb>>\\usepackage<<amsmath>>\\usepackage<<siunitx>>\\usepackage<<tikz>>''' + '''
        \\usetikzlibrary<<''' + tikz_tikzlibraries + '''>>'''
    )
chcko-{author_id}/setup.py
    import os
    import io
    import setuptools
    from pathlib import Path
    package_root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(package_root)
    try:
        import shutil
        shutil.rmtree('build')
    except:
        pass
    proot = Path(package_root)
    readme_filename = os.path.join(package_root, "README.rst")
    with io.open(readme_filename, encoding="utf-8") as readme_file:
        readme = readme_file.read()
    setuptools.setup(
        name="chcko-{author_id}",
        version = "0.1.1",
        description="{author_id} problems for chcko",
        long_description=readme,
        long_description_content_type="text/x-rst",
        author="{author_name}",
        author_email="{author_email}",
        url="{origin}",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
            "Topic :: Internet",
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Education',
            'Topic :: Education :: Computer Aided Instruction (CAI)'
        ],
        packages=setuptools.find_namespace_packages(),
        include_package_data=True,
        namespace_packages=["chcko"],
        install_requires=[],#don't ["chcko"], because on gcloud chcko is uploaded and not installed
        extras_require={},
        zip_safe=False,
    )
chcko-{author_id}/chcko/{author_id}/__init__.py
chcko-{author_id}/chcko/{author_id}/a/__init__.py
    from random import sample
    from chcko.chcko.hlp import Struct, norm_int as norm
    def given():
        a, c = sample(list(range(2, 9)) + list(range(-9, -2)), 2)
        x = sample(list(range(2, 9)) + list(range(-9, -2)), 1)[0]
        b = (c - a) * x
        g = Struct(a=a, b=b, c=c)
        return g
    def calc(g):
        res = g.b / (g.c - g.a)
        return [res]
chcko-{author_id}/chcko/{author_id}/a/en.html
    %path = "maths/linear equation/with integers"
    %kind = kinda["problems"]
    %level = 9
    \[{{g.a}} x {{util.sgn(g.b)}} {{abs(g.b)}} = {{g.c}} x\]
    <br>
    x=
    %include('chcko/getorshow')
"""
def gitget(what,get='--global'):
    try:
        return check_output(['git','config',get,what]).strip().decode()
    except:
        return ' '
def init_content(init):
    txds = txdirstr.replace('{{','{{{{').replace('}}','}}}}').replace('{}','{{}}').format(
      author_id=init
      ,author_name=gitget('user.name')
      ,author_email=gitget('user.email')
      ,author_lang='en'
      ,origin=gitget('remote.origin.url','--get')
    ).replace('<<','{').replace('>>','}')
    to_tree(txds.splitlines())

def main(**args):
    if not args:
        parser = argparse.ArgumentParser(
            description =
            '''runs chcko server, if no parameters, else see parameter list.'''
        )
        parser.add_argument(
            '-i',
            '--init',
            action='store',
            help='''provide author id to initialize a content package chcko-<author_id>''')
        parser.add_argument(
            '-s',
            '--server',
            action='store',
            help='''run chcko server (default is gunicorn)''')
        args, left = parser.parse_known_args()
        args = {k:v for k,v in args.__dict__.items() if v}
        sys.argv = sys.argv[:1]+left
    if not args:
        args['server'] = 'gunicorn'
    if 'server' in args:
        run_server(args.pop('server'))
        return
    if 'init' in args:
        init = args.pop('init')
        if init:
            init_content(init)

if __name__ == '__main__':
    main()

