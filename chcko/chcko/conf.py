# -*- coding: utf-8 -*-
'''
Sphinx setting.
'''

extensions = [
    'chcko.chcko.inl',
    'sphinx.ext.mathjax',
    'sphinxcontrib.tikz',
    'sphinxcontrib.texfigure']

# i.e. same as conf.py and with page.html containing only {{body}}
import os
templates_path = [os.path.dirname(__file__)]
del os

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

default_role = 'math'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

tikz_proc_suite = 'ImageMagick'
tikz_tikzlibraries = 'arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    'preamble': '''\\usepackage{amsfonts}\\usepackage{amssymb}\\usepackage{amsmath}\\usepackage{siunitx}\\usepackage{tikz}'''
    + '''
    \\usetikzlibrary{''' + tikz_tikzlibraries + '''}'''
}

# latex
# sphinx-build[2] -b latex -c . -D master_doc=<rst-file> -D project=<rst-file> <src-dir> <build-dir>
# sphinx-build2 -b latex -c . -D master_doc=vector -D project=vector r/b _build

# html
# sphinx-build[2] -b html -c . -D master_doc=<rst-file> -D project=<rst-file> <src-dir> <build-dir>
# sphinx-build2 -c . -D master_doc=vector -D project=vector r/b _build



