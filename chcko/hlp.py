# -*- coding: utf-8 -*-

import sys
import os.path
import importlib
import string

try:
    from itertools import izip_longest as zip_longest
except:
    from itertools import zip_longest
from collections import Iterable
from functools import wraps

from sympy import sstr, Rational as R, S, E

def ziplongest(*args):
    '''zip_longest with last element as filler
    >>> args=([9],[2,3],1)
    >>> [t for t in ziplongest(*args)]
    [(9, 2, 1), (9, 3, 1)]

    '''
    iterable = lambda a: (a if isinstance(a, Iterable) else [a])
    _args = [iterable(a) for a in args]
    withnone = zip_longest(*_args)
    for e in withnone:
        yield tuple((en or _args[i][-1]) for i, en in enumerate(e))


def listable(f):
    '''apply f to list members
    >>> @listable
    ... def mul(a,b):
    ...     'returns a*b'
    ...     return a*b
    >>> mul(2,[3,9])
    [6, 18]
    >>> mul.__doc__
    'returns a*b'

    '''
    @wraps(f)  # without this e.g __doc__ would get hidden
    def to_elems(*args, **kwargs):
        if any(isinstance(x, list) for x in args):
            return [f(*a, **kwargs) for a in ziplongest(*args)]
        else:
            return f(*args, **kwargs)
    return to_elems


def last(obj):
    @wraps(obj)
    def memoizer(*args, **kwargs):
        if len(args) + len(kwargs) != 0:
            obj.last = obj(*args, **kwargs)
        return obj.last
    return memoizer


@listable
def equal_eq(a, r):
    return a == r


@listable
def equal_0(a, r):
    try:
        res = S(a + '-(' + r + ')') == 0
    except:
        res = False
    return res


@listable
def norm_int(x):
    '''normal int string representation
    >>> norm_int('') == ''
    True
    >>> x='\t  2.0'
    >>> norm_int(x)
    '2'
    >>> x='-2.0'
    >>> norm_int(x)
    '-2'
    >>> x='-2.2'
    >>> norm_int(x)
    '-2.2'

    '''
    try:
        r = R(str(x))
        if r.is_Integer:
            return str(r)
        else:
            return str(x)
    except:
        return str(x)


@listable
def norm_frac(x):
    '''normal fraction string representation
    >>> norm_frac('')==''
    True
    >>> x='2.0'
    >>> norm_frac(x)
    '2'
    >>> x='0.125'
    >>> norm_frac(x)
    '1/8'
    >>> x='  \t 2.0'
    >>> norm_frac(x)
    '2'

    '''
    try:
        r = R(str(x))
        r = r.limit_denominator(2000)
        return str(r)
    except:
        return str(x)


@listable
def norm_rounded(x, r=2):
    '''normal rounded float representation
    >>> x,r = '2.2030023',2
    >>> norm_rounded(x,r)
    '2.20'
    >>> x,r = '3/20',2
    >>> norm_rounded(x,r)
    '0.15'
    >>> x,r = '.3/20',2
    >>> norm_rounded(x,r)
    '0.01'

    '''
    try:
        frmt = '{{:.{0}f}}'.format(r)
        res = frmt.format(float(R(str(x))))
        return res
    except:
        return x


@listable
def norm_set(x, norm=norm_rounded):
    '''
    >>> x,r = '9.33,2.2030023',0
    >>> norm_set(x,lambda v:norm_rounded(v,r))
    '2,9'
    >>> x,r = '9.32.2033',0
    >>> norm_set(x,lambda v:norm_rounded(v,r))
    '9.32.2033'

    '''
    res = [x]
    try:
        res = sorted([norm(aa) for aa in x.split(',')])
    except:
        pass
    return ','.join(res)


@listable
def norm_list(x, norm=norm_rounded):
    '''
    >>> x,r = '9.33,2.2030023',1
    >>> norm_list(x,lambda v:norm_rounded(v,r))
    '9.3,2.2'
    >>> x,r = '9.332.2023',1
    >>> norm_list(x,lambda v:norm_rounded(v,r))
    '9.332.2023'

    '''
    res = [x]
    try:
        res = [norm(aa) for aa in x.split(',')]
    except:
        pass
    return ','.join(res)


@listable
def norm_expr(a):
    '''
    >>> a = '1/4*e^(4x+4)'
    >>> norm_expr(a)
    'exp(4*x + 4)/4'

    '''
    try:
        from sympy.parsing.sympy_parser import (
            parse_expr,
            standard_transformations,
            convert_xor,
            implicit_multiplication_application)
        res = parse_expr(a, transformations=(
            standard_transformations + (convert_xor, implicit_multiplication_application,)))
        res = sstr(res.subs('e', E))
    except:
        res = a
    return res

BASE26 = string.ascii_lowercase
int_to_base26 = lambda n: int_to_base(n, BASE26, len(BASE26))
base26_to_int = lambda n: base_to_int(n, BASE26, len(BASE26))


def int_to_base(n, base, lenb):
    '''
    >>> int_to_base26(30)
    'be'

    '''
    if n < lenb:
        return base[n]
    else:
        q, r = divmod(n, lenb)
        return int_to_base(q, base, lenb) + base[r]


def base_to_int(s, base, lenb):
    '''
    >>> base26_to_int('be')
    30

    '''
    num = 0
    for char in s:
        num = num * lenb + base.index(char)
    return num


def counter():
    cnt = -1
    while True:
        cnt += 1
        yield cnt


class Struct(dict):

    '''Access dict entries as attributes.
    >>> ad = Struct(a=1,b=2); ad
    {'a': 1, 'b': 2}
    >>> ad.a, ad.b
    (1, 2)
    >>> bd = Struct()
    >>> bd = ad + bd; bd #empty defaults to 0
    {'a': 1, 'b': 2}
    >>> bd += ad; bd
    {'a': 2, 'b': 4}

    '''

    def __init__(self, *args, **kwargs):
        super(Struct, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __add__(self, other):
        return Struct(**{x: getattr(self, x, 0) + getattr(other, x, 0)
                      for x in self})

    def __iadd__(self, other):
        self.update({x: getattr(self, x, 0) + getattr(other, x, 0)
                    for x in self})
        return self


def import_module(name):
    return importlib.import_module('chcko.' + name, package='chcko')


def from_py(m):
    d = Struct(given=getattr(m, 'given', lambda: Struct()),
               calc=getattr(m, 'calc', lambda g: []),
               norm=getattr(m, 'norm', norm_rounded),
               equal=getattr(m, 'equal', equal_eq),
               points=getattr(m, 'points', None))
    try:  # get other static data not stored in db, like names of variables
        dd = {e: getattr(m, e) for e in m.__all__ if e not in d.keys()}
        d.update(dd)
    except:
        pass
    return d


class resolver:

    '''resove included template names and decide about

    Template names use '.' as path separators in python style, even if without python code.
    This allows use in URL query string.

    Template names with '/' are used in %include statements in templates, if it is not
    a content template, but helper functionality.

    >>> query_string = "test.t_1"
    >>> r = resolver(query_string,'en')
    >>> r.modulename
    'test.t_1'
    >>> os.path.basename(r.templatename)
    'en.html'
    >>> query_string = "content"
    >>> resolver(query_string,'en').modulename is 'content'
    True
    >>> query_string = "getorshow"
    >>> os.path.basename(resolver(query_string,'en').templatename)
    'getorshow.html'
    >>> query_string = "any"
    >>> os.path.basename(resolver(query_string,'en').templatename)
    ''
    >>> query_string = "test.t_1&wrong.x"
    >>> os.path.basename(resolver(query_string,'en').templatename)
    ''

    '''

    def __init__(self, query_string, lang):
        #lang = 'en'
        self.lang = lang
        self.query_string = query_string
        if self.composed():
            self.full = query_string
            self.modulename = None
            self.isdir = False
            self.has_init = False
            self.templatename = ''
        else:
            self.full = os.path.join(
                os.path.dirname(__file__),
                query_string.replace(
                    '.',
                    os.sep))
            self.isdir = os.path.isdir(self.full)
            self.has_init = os.path.exists(
                os.path.join(
                    self.full,
                    '__init__.py'))
            if self.isdir and self.has_init:
                self.modulename = query_string
            else:
                self.modulename = None
            if not self.isdir:
                self.templatename = self.full + '.html'
                if not os.path.exists(self.templatename):
                    self.templatename = ''
            else:
                for t in [lang, '_' + lang, 'x_', '_x_', 'en', '_en']:
                    self.templatename = os.path.join(self.full, t + '.html')
                    if os.path.exists(self.templatename):
                        break

    def composed(self):
        return  any([ch in self.query_string for ch in '&=%$\n'])

    def load(self):
        if self.modulename:
            m = import_module(self.modulename)
        else:
            m = Struct()
        d = from_py(m)
        return d

    def __str__(self):
        return self.query_string + '=>' + \
            str((self.modulename, self.templatename))


def mklookup(lang):
    return lambda n: resolver(n, lang).templatename

datefmt = lambda dt: dt.isoformat(' ').split('.')[0]

PAGES = [
    'content',
    'contexts',
    'done',
    'edits',
    'login',
    'main',
    'message',
    'password',
    'signup',
    'static',
    'todo',
    'verification',
    'forgot']

def author_folder(fn, withtest=False):
    ''' checks whether fn is an author's content folder
    >>> author_folder('_no')
    False
    >>> author_folder('yes')
    True
    >>> author_folder('main') # is in PAGES
    False
    >>> author_folder('n.o')
    False
    '''
    return (fn not in PAGES + (['test'] if withtest else [])
            and not fn.startswith('_') and '.' not in fn)


is_standard_server = False
if os.getenv('GAE_ENV', '').startswith('standard'):
  is_standard_server = True

