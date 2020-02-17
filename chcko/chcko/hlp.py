# -*- coding: utf-8 -*-

import sys
import os
import importlib
import string
import datetime
from itertools import chain
from urllib.parse import parse_qsl
try:
    from itertools import izip_longest as zip_longest
except:
    from itertools import zip_longest
from collections.abc import Iterable
from functools import wraps

import chcko
from chcko.chcko.bottle import SimpleTemplate
from chcko.chcko.languages import langkindnum, langnumkind, kindint
from chcko.chcko.auth import (
  gen_salt
  ,jwtcode
  ,random_student_path
  ,generate_password_hash
  ,check_password_hash
)

from sympy import sstr, Rational as R, S, E

import logging
logger = logging.getLogger('chcko')
logger.addHandler(logging.NullHandler())

def authordirs():
    dirs = []
    for x in chcko.__path__:
        for y in os.listdir(x):
            xy = os.path.join(x,y)
            if xy.endswith('chcko'):
                continue
            if os.path.exists(os.path.join(xy,'__init__.py')):
                dirs.append(xy)
    return set(dirs)
AUTHORDIRS = authordirs()

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


def chcko_import(name):
    m = importlib.import_module('chcko.'+name)
    return m


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


def template_from_path(qspath, lang):
    for t in [lang, '_' + lang, 'x_', '_x_', 'en', '_en']:
        templatename = os.path.join(qspath, t + '.html')
        if os.path.exists(templatename):
            return templatename
    return ''

class resolver:
    def __init__(self, query_string, lang):
        self.lang = lang
        self.query_string = query_string
        self.composed = any([ch in self.query_string for ch in '&=%$\n'])
        self.templatename = ''
        self.modulename = ''
    def load(self):
        if not self.composed:
            self.modulename = self.query_string
            try:
                m = chcko_import(self.modulename)
                qspath = list(m.__path__)
                for qsp in qspath:
                    self.templatename = template_from_path(qsp,self.lang)
                    if self.templatename:
                        break
            except ModuleNotFoundError:
                self.modulename = ''
                m = Struct()
        else:
            m = Struct()
        d = from_py(m)
        return d

def mklookup(lang):
    def get_templatename(n):
        templatename = ''
        for pkgdir in chcko.__path__:
            npath = os.path.join(pkgdir,n.replace('.',os.sep))
            if os.path.isdir(npath):
                templatename = template_from_path(npath,lang)
            else:
                templatename = npath + '.html'
                if not os.path.exists(templatename):
                    templatename = ''
            if templatename:
                return templatename
        rsv = resolver(n, lang)
        rsv.load()
        return rsv.templatename
    return get_templatename

datefmt = lambda dt: dt.isoformat(' ').split('.')[0]

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
def filter_student(querystring):
    '''filter out student_contexts and color
    >>> querystring = 'School=b&Period=3&Teacher=5e&Class=9&Student=0&color=#E&bm&ws>0,d~1&b.v=3'
    >>> filter_student(querystring)
    'bm&ws>0,d~1&b.v=3'

    '''
    qfiltered = [x  for x in
            parse_qsl(querystring, True)
            if x[0] not in student_contexts + ['color']]
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

student_contexts = ['School', 'Period', 'Teacher', 'Class', 'Student']
problem_contexts = student_contexts + ['Problem']

class db_mixin:
    def urlstring(self,key):
        #'School=myschool&Period=myperiod&Teacher=myteacher&Class=myclass&Student=myself'
        return '&'.join([r + '=' + str(v) for r, v in key.pairs()])

    def init_db(self):
        self.clear_index()
        self.available_langs = []
        self.student_contexts = student_contexts
        chckopackages = set(os.path.basename(chckopath) for chckopath in AUTHORDIRS)
        chckopackages = chckopackages - set(['chcko'])
        for chckop in chckopackages:
            initdbmod = chckop+'.initdb'
            initdb = chcko_import(initdbmod)
            self.available_langs.extend(initdb.available_langs)
            initdb.populate_index(
                lambda problemid, lang, kind, level, path: self.Index.get_or_insert(
                        problemid + ':' + lang,
                        knd=int(kind),
                        level=int(level),
                        path=path)
                )
        self.available_langs = set(self.available_langs)

    def problem_create(self,student,**pkwargs):
        return self.Problem.create(parent=student.key,
                  **{s: pkwargs[s] for s in self.columnsof(self.Problem) if s in pkwargs})
    def problem_set(self,problem):
        return self.allof(self.query(self.Problem,[self.Problem.collection==self.idof(problem)],self.Problem.nr))
    def problem_by_query_string(self,query_string,lang,student):
        res = self.first(self.query(
            self.Problem,[self.Problem.query_string==query_string,
                      self.Problem.lang==lang,
                      self.Problem.answers==None], parent=self.idof(student)))
        return res
    def clear_student_problems(self,student):
        self.delete_query(self.query(self.Problem,parent=self.idof(student)))
    def student_assignments(self,student):
        return self.query(self.Assignment,parent=self.idof(student))
    def del_stale_open_problems(self,student,age):
        self.delete_query(self.query(self.Problem,[self.Problem.answered==None,
                                         self.Problem.created<age],parent=self.idof(student)))
        self.delete_query(self.query(self.Problem,[self.Problem.concatanswers=='',
                                         self.Problem.answered!=None],parent=self.idof(student)))
    #def clear_unanswered_problems(self):
    #    self.delete_query(self.query(self.Problem,[self.Problem.answers==None]))
    def assign_to_student(self, studentkeyurlsafe, query_string, duedays):
        studentkey = self.Key(urlsafe=studentkeyurlsafe)
        query_string=normqs(query_string)
        now = datetime.datetime.now()
        due=now+datetime.timedelta(days=int(duedays))
        assgn = self.Assignment.create(parent=studentkey
                   ,query_string=query_string
                   ,due=due)
        self.save(assgn)
    def del_collection(self,problem):
        self.delete_query(self.query(self.Problem,[self.Problem.collection==self.idof(problem)]))
        self.delete_query(self.query(self.Problem,[self.idof(self.Problem)==self.idof(problem)]))
    def copy_to_new_student(self,oldparent, newparent):
        self.copy_to_new_parent(self.Problem, oldparent, newparent)
        self.copy_to_new_parent(self.Assignment, oldparent, newparent)

    def add_student(self, studentpath=[None]*5, user=None, color=None):
        userkey = user and self.idof(user) or None
        school_, period_, teacher_, class_, student_ = studentpath
        school = self.School.get_or_insert(
            school_ or 'myschool',
            userkey=userkey)
        period = self.Period.get_or_insert(
            period_ or 'myperiod',
            parent=school.key,
            userkey=userkey)
        teacher = self.Teacher.get_or_insert(
            teacher_ or 'myteacher',
            parent=period.key,
            userkey=userkey)
        clss = self.Class.get_or_insert(
            class_ or 'myclass',
            parent=teacher.key,
            userkey=userkey)
        stdnt = self.Student.get_or_insert(
            student_ or 'myself',
            parent=clss.key,
            userkey=userkey,
            color=color or '#EEE')
        if stdnt.userkey == userkey and (color and stdnt.color != color):
            stdnt.color = color
            self.save(stdnt)
        return stdnt

    def key_from_path(self,x):
        return self.Key(*list(chain(*zip(problem_contexts[:len(x)], x))))
    def from_urlsafe(self,urlsafe):
        try:
          obj = self.Key(urlsafe=urlsafe).get()
          return obj
        except:
          return None
    def clear_index(self):
        self.delete_query(self.query(self.Index))
    def clear_problems(self):
        self.delete_query(self.query(self.Problem))
    def problem_from_resolver(self, rsv, nr, student):
        d = rsv.load()
        g = d.given()
        r = d.norm(d.calc(g))
        pkwargs = d.__dict__.copy()
        points = d.points or [1] * len(r or [])
        pkwargs.update(dict(
            g=g,
            answered=None,
            lang=rsv.lang,
            query_string=rsv.query_string,
            nr=nr,
            results=r,
            given=g,
            inputids=["{:0=4x}".format(nr) + "_{:0=4x}".format(a) for a in range(len(r))],
            points=points
        ))
        problem = self.problem_create(student,**pkwargs)
        return problem, pkwargs
    def clear_assignments(self):
        self.delete_query(self.query(self.Assignment))
    def clear_student_assignments(self,student):
        self.delete_query(self.student_assignments(student))
    def clear_done_assignments(self, student, usr):
        todelete = []
        for anobj in self.assign_table(student, usr):
            if self.done_assignment(anobj):
                todelete.append(anobj.key)
        self.delete_keys(todelete)
    def clear_all_data(self):
        self.clear_index()
        self.clear_assignments()
        self.clear_problems()
        self.delete_query(self.query(self.Student))
        self.delete_query(self.query(self.Class))
        self.delete_query(self.query(self.Teacher))
        self.delete_query(self.query(self.Period))
        self.delete_query(self.query(self.School))
        self.add_student()
    def assignable(self, teacher, usr):
        for akey in self.depth_1st(keys=[teacher.key], kinds='Teacher Class Student'.split(),
                              userkey=usr and self.idof(usr)):
            yield akey
    def assign_table(self,student, usr):
        for e in self.depth_1st(keys=[student.key], kinds='Student Assignment'.split(),
                           userkey=usr and self.idof(usr)):
            yield e
    def student_roles(self, usr):
        students = self.allof(self.query(self.Student,[self.Student.userkey==self.idof(usr)]))
        for student in students:
            yield self.key_ownd_path(student, usr)
    def key_ownd_path(self, student, usr):
        userkey = usr and self.idof(usr)
        skey = student.key
        key_ownd_list = [(skey, student.userkey == userkey)]
        parentkey = skey.parent()
        while parentkey and parentkey.pairs():
            key_ownd_list = [(parentkey, parentkey.get().userkey == userkey)] + key_ownd_list
            parentkey = parentkey.parent()
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
                  , kinds=problem_contexts
                  , permission=False
                  , userkey=None
                  ):
        ''' path entries are names or filters ([] for all)
        translated into record objects along the levels given by **kinds** depth-1st-wise.

        Yields objects, not keys.

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
        modliname = self.kindof(modli)
        parentkey = keys and keys[-1] or None
        parentobj = parentkey and parentkey.get() or None
        permission = permission or parentobj and parentobj.userkey == userkey
        if isinstance(pathi,str):
            k = self.Key(modliname, pathi, parent=parentkey)
            obj = k.get()
            if obj:
                yield obj
                if i < N - 1:
                    keys.append(k)
                    for e in self.depth_1st(path, keys, kinds, permission, userkey):
                        yield e
                    del keys[-1]
        elif permission:
            filt = [self.filter_expression(ap, op, av) for ap, op, av in pathi if ap in modliprops]
            ordr = None
            if modli == self.Problem:
                ordr = self.Problem.answered
            elif 'created' in modliprops:
                ordr = modli.created
            allrecs = self.allof(self.query(modli,filt,ordr,parent=self.idof(parentobj)))
            for obj in allrecs:
                k = obj.key
                yield obj
                if i < N - 1:
                    keys.append(k)
                    for e in self.depth_1st(path, keys, kinds, permission):
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

        >>> from chcko.chcko.db import db
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
        idx = self.allof(self.query(self.Index))
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
            if len(self.problem_set(e)):
                return [datefmt(e.answered), e.answers]
            else:
                return [datefmt(e.answered), [bool(x) for x in e.oks], e.answers, e.results]
        elif isinstance(e, self.Student):
            return ['', '', '', '', e.key.string_id()]
        elif isinstance(e, self.Class):
            return ['', '', '', e.key.string_id()]
        elif isinstance(e, self.Teacher):
            return ['', '', e.key.string_id()]
        elif isinstance(e, self.Period):
            return ['', e.key.string_id()]
        elif isinstance(e, self.School):
            return [e.key.string_id()]
        elif isinstance(e, self.Assignment):
            now = datetime.datetime.now()
            overdue = now > e.due
            return [(datefmt(e.created), e.query_string), datefmt(e.due), overdue]
        # elif e is None:
        #    return ['no such object or no permission']
        return []
    def set_student(self,request,response):
        '''There is always a student role

        - There is a student role per client without user
        - There are more student roles for a user with one being current

        None or a redirect string for a message is returned.

        '''
        try:
            usr = request.user
        except:
            usr = None
        student = None
        studentpath = [request.params.get(x,'') for x in student_contexts]
        color = request.params.get('color','')
        request.query_string = filter_student(request.query_string)
        if ''.join(studentpath) != '':
            student = self.add_student(studentpath, usr, color)
            if student.userkey != self.idof(usr):
                # student role does not belong to user, so don't change current student
                student = None
                return 'message?msg=e'
        elif usr:
            student = self.current_student(usr)
        if not student:
            chckostudenturlsafe = request.get_cookie('chckostudenturlsafe')
            if chckostudenturlsafe:
                student = self.from_urlsafe(chckostudenturlsafe)
                if student and usr:
                    if student.userkey != self.idof(usr):
                        student = None
        if not student and usr:
            student = self.first(self.query(self.Student,[self.Student.userkey==self.idof(usr)]))
        if not student:  # generate
            studentpath = random_student_path(seed=request.remote_addr).split('-')
            student = self.add_student(studentpath, usr, color)
        if usr and student:
            if not usr.current_student or (usr.current_student != self.idof(student)):
                usr.current_student = self.idof(student)
                self.save(usr)
        if student:
            self.set_cookie(response,'chckostudenturlsafe',self.urlsafe(student.key))
            SimpleTemplate.defaults["contextcolor"] = student.color or '#EEE'
            request.student = student

    def set_cookie(self,response,cookie,value):
        response.set_cookie(cookie,value,httponly=True,path='/',samesite='strict',maxage=datetime.timedelta(days=30))

    def set_user(self,request):
        request.user = None
        chckousertoken = request.get_cookie('chckousertoken')
        if chckousertoken and chckousertoken!='null':
            request.user = self.user_by_token(chckousertoken)
        if request.user is None:
            tkn = request.params.get('token')
            request.user = self.user_by_token(tkn)

    def token_delete(self, token):
        self.delete_keys([self.token_key(token)])
    def token_create(self, email):
        token = gen_salt()
        key = self.token_key(token)
        usrtkn = self.UserToken.create(id=key, email=email)
        self.save(usrtkn)
        return token
    def token_insert(self,jwt,email):
        token = jwtcode(jwt).decode()
        usrtkn = self.UserToken.create(id=token, email=email)
        self.save(usrtkn)
        return token
    def token_key(self, token):
        return self.Key(self.UserToken, token)
    def token_validate(self,token):
        return self.token_key(token).get() is not None
    def user_by_token(self, token):
        usrtkn = token and self.token_key(token).get()
        usr = None
        if usrtkn:
            usr = self.Key(self.User, usrtkn.email).get()
        return usr
    def user_email(self,usr):
        return usr.key.string_id()
    def user_name(self,usr):
        return usr.fullname or self.user_email(usr)
    def user_set_password(self, usr, password):
        usr.pwhash = generate_password_hash(password)
        self.save(usr)
    def is_social_login(self,usr):
        return usr.pwhash == ''
    def user_login(self, email, fullname, password=None, token=None):
        usr = self.Key(self.User,email).get()
        if usr:
            if password is not None and token is None:
                if not check_password_hash(usr.pwhash,password):
                    raise ValueError("User exists and has different password")
            elif token is not None:
                #there is always just one way to log in,
                #here switch from password to social
                usr.pwhash = ''
                usr.token = token
                usr.verified = True
                self.save(usr)
            token = usr.token
        else:
            if token is None and password is not None:
                token = self.token_create(email)
                usr = self.User.get_or_insert(email, pwhash=generate_password_hash(password), fullname=fullname, token=token, verified=False)
            elif token is not None:
                #token comes from token_insert(), which is called before user_login()
                usr = self.User.get_or_insert(email, pwhash='', fullname=fullname, token=token, verified=True)
        return usr,token
    def set_answer(self,problem,answers):
        problem.answers = answers
        problem.concatanswers = ''.join(answers)

rindex = lambda al,a: len(al) - al[-1::-1].index(a)-1
def check_test_answers(m=None, norm_inputs=None):
    '''Call ``given()``, ``calc()`` and ``norm()`` once.
    Then apply norm to different test inputs.
    This verifies that none raises an exception.

    m can be module or __file__ or None

    For interactive use with globals:
    >>> norm_inputs = [['2haa'],['2,2.2'],['2,2/2']]
    >>> check_test_answers(None,norm_inputs)

    For use in a pytest test_xxx function
    >>> check_test_answers(__file__,norm_inputs)

    '''
    if m is None:
        m = Struct()
        m.update(globals())
    elif isinstance(m, str):
        #m = __file__
        thisdir = os.path.dirname(os.path.abspath(m))
        splitpath = thisdir.split(os.sep)
        auth_prob = splitpath[rindex(splitpath,'chcko') + 1:]
        if not auth_prob:
            return
        pyprob = os.path.join(*auth_prob).replace(os.sep, '.')
        m = chcko_import(pyprob)
    d = from_py(m)
    g = d.given()
    norm_results = d.norm(d.calc(g))
    if norm_inputs:
        for t in norm_inputs:
            d.norm(t)
