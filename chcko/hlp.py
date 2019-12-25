# -*- coding: utf-8 -*-

import sys
import os.path
import importlib
import string
from urllib.parse import parse_qsl

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
    try:  # get other static data not stored, like names of variables
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

def normqs(qs):
    '''take away =1 from a content query

    >>> qs = 'r.bm=1'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm=2'
    >>> normqs(qs)
    'r.bm=2'
    >>> qs = 'r.bm'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm&r.x=1'
    >>> normqs(qs)
    'r.bm&r.x=1'

    '''
    qparsed = parse_qsl(qs, True)
    if len(qparsed) == 1 and qparsed[0][1] == '1':
        return qparsed[0][0]
    return qs
def filter_student(self,querystring):
    '''filter out student_contexts and color
    >>> querystring = 'School=b&Period=3&Teacher=5e&Class=9&Student=0&color=#E&bm&ws>0,d~1&b.v=3'
    >>> filter_student(querystring)
    'bm&ws>0,d~1&b.v=3'

    '''
    qfiltered = [x  for x in
            parse_qsl(querystring, True)
            if x[0] not in self.student_contexts + ['color']]
    qsfiltered = '&'.join([k + '=' + v if v else k for k, v in qfiltered])
    return qsfiltered



def key_value_leaf_id(p_ll):  # key_value_leaf_depth
    '''
    >>> p_ll = [('a/b','ab'),('n/b','nb'),('A/c','ac')]
    >>> [(a,b,c,d) for a, b, c, d in list(key_value_leaf_id(p_ll))]
    [('a', '1a'), ('b', '2a'), ('c', '2b'), ('n', '1b'), ('b', '2a')]

    '''
    previous = []
    depths = []
    for p, ll in sorted(p_ll, key=lambda v:v[0].lower()):
        keypath = p.split('/')
        this = []
        nkeys = len(keypath)
        for depth, kk in enumerate(keypath):
            if depth >= len(depths):
                depths.append(0)
            this.append(kk)
            if [x.lower() for x in this] < [x.lower() for x in previous]:
                continue
            else:
                del depths[depth+1:]
                lvl_id = str(depth + 1) + int_to_base26(depths[depth])
                depths[depth] = depths[depth] + 1
                yield (kk, ll, depth == nkeys - 1, lvl_id)
                previous = this[:]

_student_contexts = ['School', 'Period', 'Teacher', 'Class', 'Student']
_problem_contexts = ['School', 'Period', 'Teacher', 'Class', 'Student', 'Problem']

class db_mixin:
    def urlstring(self,key):
        #'School=myschool&Period=myperiod&Teacher=myteacher&Class=myclass&Student=myself'
        return '&'.join([r + '=' + str(v) for r, v in key.pairs()])
    def init_db(self):
        from chcko import initdb
        self.available_langs = initdb.available_langs
        with self.dbclient.context():
            self.clear_students()
            initdb.populate_index(
                lambda problemid, lang, kind, level, path: Index.get_or_insert(
                        problemid + ':' + lang,
                        knd=int(kind),
                        level=int(level),
                        path=path)
                )

    def problem_set(self,problem):
        return self.allof(self.query(self.Problem,[self.Problem.collection==self.idof(problem)],self.Problem.nr))
    def problem_by_query_string(self,query_string,lang,student):
        return self.first(self.query(
            self.Problem,[self.Problem.query_string==query_string,
                      self.Problem.lang==lang,
                      self.Problem.answer==None,
                      self.of(self.Problem)==self.idof(student)]
            ))
    def clear_student_problems(self,student):
        self.delete(self.query(self.Problem,[self.of(self.Problem)==self.idof(student)]))
    def clear_unanswered_problems(self):
        self.delete(self.query(self.Problem,[self.Problem.answers==None]))
    def student_assignments(self,student):
        return self.query(self.Assignment,[self.of(self.Assignment)==self.idof(student)])
    def del_stale_open_problems(self,student,age):
        self.delete(self.query(self.Problem,[self.Problem.answered==None,
                                         self.Problem.created<age,self.of(self.Problem)==self.idof(student)]))
        self.delete(self.query(self.Problem,[self.Problem.answersempty==True,
                                         self.Problem.answered!=None,self.of(self.Problem)==self.idof(student)]))
    def del_collection(self,problem):
        self.delete(self.query(self.Problem,[self.Problem.collection==self.idof(problem)]))
        self.delete(self.query(self.Problem,[self.idof(self.Problem)==self.idof(problem)]))
    def copy_to_new_student(self,oldparent, newparent):
        self._copy_to_new_parent(self.Problem, oldstudent, self.request.student)
        self._copy_to_new_parent(self.Assignment, oldstudent, self.request.student)

    def key_from_path(self,x):
        return self.Key(*list(chain(*zip(_problem_contexts[:len(x)], x))))
    def from_urlsafe(urlsafe):
        return self.Key(urlsafe=urlsafe).get()
    def clear_index(self):
        self.delete(self.Index.query())
    def clear_problems(self):
        self.delete(self.Problem.query())
    def problem_from_resolver(self, rsv, nr, student):
        '''create a problem from a resolver (see hlp.py)
        '''
        d = rsv.load()
        g = d.given()
        r = d.norm(d.calc(g))
        pkwargs = d.__dict__.copy()
        pkwargs.update(dict(
            g=g,
            answered=None,
            lang=rsv.lang,
            query_string=rsv.query_string,
            nr=nr,
            results=r,
            given=g,
            inputids=["{:0=4x}".format(nr) + "_{:0=4x}".format(a) for a in range(len(r))],
            points=d.points or [1] * len(r or [])
        ))
        problem = self.problem_create(student,**pkwargs)
        return problem, pkwargs
    def clear_assignments(self):
        self.delete(self.Assignment.query())
    def clear_students(self):
        self.delete(self.Student.query())
        self.delete(self.Class.query())
        self.delete(self.Teacher.query())
        self.delete(self.Period.query())
        self.delete(self.School.query())
        self._add_student()
    def clear_student_assignments(self,student):
        self.delete(self.student_assignments(student))
    def clear_done_assignments(self, student, user):
        for anobj in self.assign_table(student, user):
            if done_assignment(anobj):
                anobj.key.delete()
    def done_assignment(self,assignm):
        q = self.query(self.Problem, [self.of(self.Problem)==self.idof(assignm),
                                 self.Problem.query_string == normqs(assignm.query_string),
                                 self.Problem.answered > assignm.created])
        if q.count() > 0:
            return True
        else:
            return False
    def assignable(self, teacher, user):
        for akey in depth_1st(keys=[teacher.key], kinds='Teacher Class Student'.split(),
                              userkey=user and user.key):
            yield akey
    def assign_table(student, user):
        for e in depth_1st(keys=[student.key], models='Student Assignment'.split(),
                           userkey=user and user.key):
            yield e
    def student_roles(self, user):
        students = self.allof(self.query(self.Student,[self.Student.userkey==self.idof(user)]))
        for student in students:
            yield self.key_ownd_path(student, user)
    def key_ownd_path(self, student, user):
        userkey = user and user.key
        key_ownd_list = [(student.key, student.userkey == userkey)]
        parent = student.parent()
        while parent:
            key_ownd_list = [(parent.key, parent.userkey == userkey)] + key_ownd_list
            parent = parent.parent()
        return key_ownd_list
    def keys_to_omit(self,path):
        "[name1,name2,nonstr,...]->[key2,key2]"
        keys = []
        boolpth = [isinstance(x, str) for x in path]
        ipth = boolpth.index(False) if False in boolpth else len(boolpth)
        if ipth > 0:
            keys = [self.key_from_path(path[:ipth])] * ipth
        return keys
    def depth_1st(self
                  , path=None
                  , keys=None  # start keys, keys_to_omit(path) to skip initial hierarchy
                  , kinds=_problem_contexts
                  , permission=False
                  , userkey=None
                  ):
        ''' path entries are names or filters ([] for all)
        translated into record objects along the levels given by **kinds** depth-1st-wise.

        >>> from chcko.db import *
        >>> from chcko.test.hlp import problems_for
        >>> #del sys.modules['chcko.test.hlp']
        >>> path = ['a', 'b', 'c', 'd', 'e']
        >>> student = _add_student(path, 'EEE')
        >>> problems_for(student)
        >>> lst = list(db.depth_1st(path+[[]]))
        >>> db.nameof(list(db.depth_1st(path+[[('query_string','=','r.u')]]))[0])
        'School'
        >>> path = ['a', 'b', 'c', 'x', 'e']
        >>> student1 = _add_student(path, 'EEE')
        >>> problems_for(student1)
        >>> path = ['a','b','c',[],[],[('query_string','=','r.u')]]
        >>> db.nameof(list(db.depth_1st(path))[0])
        'School'
        >>> db.nameof(list(db.depth_1st(path,keys=db.keys_to_omit(path)))[0])
        'Class'
        >>> list(db.depth_1st())
        []

        '''
        modl = [getattr(self,name) for name in kinds]
        N = len(modl)
        if not path:
            path = [[]] * N
        while len(path) < N:
            path += [[]]
        if keys is None:
            keys = []
        i = len(keys)
        pathi = path[i]
        modli = modl[i]
        modliprops = set(self.columnsof(modli))
        modliname = self.nameof(modli)
        parentkey = keys and keys[-1] or None
        parentobj = parentkey.get()
        permission = permission or parentobj and parentobj.userkey == userkey
        if isinstance(pathi,str):
            k = self.Key(modliname, pathi, parent=parentkey)
            obj = k.get()
            if obj:
                yield obj
                if i < N - 1:
                    keys.append(k)
                    for e in depth_1st(path, keys, kinds, permission, userkey):
                        yield e
                    del keys[-1]
        elif permission:
            filt = [self.filter_expression(ap, op, av) for ap, op, av in pathi if ap in modliprops]
            ordr = None
            if modli == self.Problem:
                ordr = self.Problem.answered
            elif 'created' in modliprops:
                ordr = modli.created
            allrecs = self.allof(self.query(modli,parentkey,filt,ordr))
            for obj in allrecs:
                k = obj.key
                yield obj
                if i < N - 1:
                    keys.append(k)
                    for e in depth_1st(path, keys, kinds, permission):
                        yield e
                    del keys[-1]
        # else:
        # yield None #no permission or no such object
    def filtered_index(self, lang, opt):
        ''' filters the index by lang and optional by

            - level
            - kind
            - path
            - link

        >>> from chcko.db import *
        >>> lang = 'en'
        >>> opt1 = [] #[('level', '2'), ('kind', 'exercise')]
        >>> cnt1 = sum([len(list(gen[1])) for gen in db.filtered_index(lang, opt1)])
        >>> opt2 = [('level', '10'),('kind','1'),('path','maths'),('link','r')]
        >>> cnt2 = sum([len(list(gen[1])) for gen in db.filtered_index(lang, opt2)])
        >>> cnt1 != 0 and cnt2 != 0 and cnt1 > cnt2
        True

        '''
        def safeint(s):
            try:
                return int(s)
            except:
                return -1
        kindnum = langkindnum[lang]
        numkind = langnumkind[lang]
        optd = dict(opt)
        knd_pathlnklvl = {}
        idx = self.allof(self.query(Index))
        for e in idx:
            # e=itr.next()
            # knd_pathlnklvl
            link, lng = e.key.string_id().split(':')
            if lng == lang:
                if 'level' not in optd or safeint(optd['level']) == e.level:
                    if 'kind' not in optd or kindint(optd['kind'],kindnum) == e.knd:
                        if 'path' not in optd or optd['path'] in e.path:
                            if 'link' not in optd or optd['link'] in link:
                                lpl = knd_pathlnklvl.setdefault(e.knd, [])
                                lpl.append((e.path, (link, e.level)))
                                lpl.sort()
        s_pl = sorted(knd_pathlnklvl.items())
        knd_pl = [(numkind[k], key_value_leaf_id(v)) for k, v in s_pl]
        #[('Problems', <generator>), ('Content', <generator>),... ]
        return knd_pl
    def table_entry(self, e):
        'what of entity e is used to render html tables'
        if isinstance(e, self.Problem) and e.answered:
            if self.problem_set(e).count():
                return [datefmt(e.answered), e.answers]
            else:
                return [datefmt(e.answered), e.oks, e.answers, e.results]
        elif isinstance(e, self.Student):
            return ['', '', '', '', self.idof(e)]
        elif isinstance(e, self.Class):
            return ['', '', '', self.idof(e)]
        elif isinstance(e, self.Teacher):
            return ['', '', self.idof(e)]
        elif isinstance(e, self.Period):
            return ['', self.idof(e)]
        elif isinstance(e, self.School):
            return [self.idof(e)]
        elif isinstance(e, self.Assignment):
            now = datetime.datetime.now()
            overdue = now > e.due
            return [(datefmt(e.created), e.query_string), datefmt(e.due), overdue]
        # elif e is None:
        #    return ['no such object or no permission']
        return []
    def set_student(self,request):
        '''There is always a student role

        - There is a student role per client without user
        - There are more student roles for a user with one being current

        Else a redirect string for a message is returned.

        '''
        user = request.user
        session = request.session
        request.student = None
        studentpath = [request.get(x,'') for x in _student_contexts]
        color = request.get('color','')
        request.query_string = filter_student(request.query_string)
        if ''.join(studentpath) != '':
            student = self._add_student(studentpath, color, user)
            if student.userkey == self.idof(user):
                request.student = student
            # student role does not belong to user, so don't change current student
            else:
                return 'message?msg=e'
        elif user:
            request.student = user.current_student and user.current_student.get()
        else:
            studentkey_nouser = session and Session['studentkey_nouser']
            if studentkey_nouser:
                try:
                    request.student = Key(
                        urlsafe=studentkey_nouser).get()
                except (TypeError, BadKeyError, AttributeError):
                    pass
        if not request.student and user:
            request.student = self.first(self.query(self.Student,[self.Student.userkey==self.idof(user)]))
        if not request.student:  # generate
            studentpath = auth.random_student_path(seed=request.remote_addr).split('-')
            request.student = self._add_student(studentpath, color, user)
        if user:
            if user.current_student.string_id() != self.idof(request.student):
                user.current_student = request.student.key
                user.put()
        elif session:
            session['studentkey_nouser'] = request.student.key.urlsafe()
        SimpleTemplate.defaults["contextcolor"] = request.student.color or '#EEE'


    def set_user(self,request):
        session = request.session
        userID = session and session['userID']
        request.user = None
        if userID:
            request.user = self.Key(urlsafe=userID).get()
    def stored_email_credential(self):
        return base64.urlsafe_b64decode(self._stored_secret('chcko.mail').encode())
    def send_mail(self, to, subject, message_text, creds, sender=auth.chcko_mail):
        auth.send_mail(to, subject, message_text, creds=self.stored_email_credential())
    def user_timestamp_by_token(self, token, subject='auth'):
        usertoken = self.User.token_model.selfmadekey(subject, token).get()
        if usertoken:
            user = self.Key(self.nameof(self.User), usertoken.email).get()
            if user:
                timestamp = int(time.mktime(usertoken.created.timetuple()))
                return user, timestamp
        return None, None
    def create_signup_token(self, email):
        return UserToken.create(email, 'signup').token
    def delete_signup_token(self, token):
        UserToken.selfmadekey('signup', token).delete()
    def create_user(self,email,password):
        return User.create(email,password)
    def user_by_login(self,email,password):
        return User.by_login(email,password)
    def validate_token(self,subject, token):
        return UserToken.selfmadekey(subject=subject,
                   token=token).get() is not None
    def validate_signup_token(self, token):
        return self.validate_token('signup', token)

