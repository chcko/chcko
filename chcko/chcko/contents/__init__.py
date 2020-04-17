# -*- coding: utf-8 -*-
"""
The contents page is the default, if no page specified.

With contents IDs::

    /<chlang>/[contents][?(<author>.<id>[=<cnt>])&...]

    /en/?r.a=2&r.bu

Without contents IDs it is an index page, which can be filter::

    /<chlang>/contents[?<filter>=<value>&...]

    /en/contents?level=10&kind=1&path=maths&link=r

See ``filtered_index`` for that.

"""

import re
import datetime
from itertools import count

from urllib.parse import parse_qsl
from chcko.chcko.bottle import SimpleTemplate, StplParser, get_tpl, HTTPError
from chcko.chcko.hlp import (
        Struct,
        resolver,
        mklookup,
        logger
)

from chcko.chcko.util import PageBase, Util

from chcko.chcko.db import db

re_id = re.compile(r"^[^\d\W]\w*(\.[^\d\W]\w*)*$", re.UNICODE)
#re_id.match('a.b') #OK
#re_id.match('a.b.c') #OK
#re_id.match('a.b.c=2') #KO
#re_id.match('a.b&c.c') #KO

codemarkers = set(StplParser.default_syntax) - set([' '])

class Page(PageBase):
    'Entry points are ``get_response`` and ``post_response``.'

    def __init__(self, mod):
        super().__init__(mod)
        self.problem = None
        self.problem_set = []
        self.chuery = self.request.query_string.replace(';','&')
        self.query_show = show_qs(self.chuery)

    def _get_problem(self, choblemkey=None):
        '''init the problem from database if it exists
        '''
        urlsafe = choblemkey or self.query_show.startswith(
            'key=') and self.query_show[4:].split('&')[0]

        if urlsafe:
            self.problem = db.from_urlsafe(urlsafe)
            if self.problem:  # else it was deleted
                if not isinstance(self.problem,db.Problem):
                    raise HTTPError(404,'404_5')
                # query_show here is "key=..."
                # replace query_show with that of the problem to load the problem in tpl_from_qs()
                self.query_show = self.problem.chuery
        else:  # get existing unanswered if problem.chuery==query_show
            self.problem = db.problem_by_chuery(
                self.query_show,
                self.request.chlang,
                self.request.student)

        if self.problem:
            keyOK = self.problem.key.parent()
            userkey = self.request.student.userkey
            while keyOK:
                thislev = keyOK.get()
                if thislev.userkey == userkey:
                    break
                elif userkey == None and thislev.userkey != None:
                    keyOK = None
                    break
                keyOK = keyOK.parent()
            if not keyOK:
                #logger.warning("%s not for %s", db.urlstring(self.problem.key), db.urlstring(self.request.student.key))
                raise HTTPError(403,'403_6')
            self.problem_set = db.problem_set(self.problem)
        elif choblemkey is None:  # XXX: Make deleting empty a cron job
            # remove unanswered problems for this user
            # timedelta to have the same problem after returning from a
            # followed link
            age = datetime.datetime.now() - datetime.timedelta(days=1)
            db.del_stale_open_problems(self.request.student,age)

    def load_content(self
                     , layout='chcko/contents'
                     , rebase=True
                     ):
        ''' evaluates the templates with includes therein and zips them to database entries

        examples:
            chcko/chcko/tests/test_content.py

        '''

        tplid = self.tpl_from_qs()
        _chain = []
        withempty, noempty = self.make_summary()
        nrs = count()
        problems_cntr = count()
        SimpleTemplate.overrides = {}
        problem_set_iter = [None]
        langlookup = mklookup(self.request.chlang)

        env = {}
        stdout = []

        def _new(rsv):
            chumber = next(nrs)
            problem, pydict = db.problem_from_resolver(
                rsv, chumber, self.request.student)
            if not self.problem:
                self.problem = problem
                self.current = self.problem
            else:
                db.add_to_set(problem,self.problem)
            if problem.choints:
                next(problems_cntr)
            db.save(problem)
            if not rsv.composed:
                SimpleTemplate.overrides.update(pydict)
                _chain[-1] = SimpleTemplate.overrides.copy()

        def _zip(rsv):
            if not self.current or rsv.chuery != self.current.chuery:
                ms = rsv.chuery
                if self.current:
                    ms += ' != ' + self.current.chuery
                #logger.info(ms)
                raise HTTPError(400,'400_7 '+ms)
            pydict = rsv.load()  # for the things not stored, like 'names'
            pydict.update(db.fieldsof(self.current))
            pydict['g'] = self.current.chiven
            if self.current.choints:
                next(problems_cntr)
            if self.current.chanswered:
                sw, sn = self.make_summary(self.current)
                pydict.update({'chummary': (sw, sn)})
                withempty.__iadd__(sw)
                noempty.__iadd__(sn)
            if not rsv.composed:
                SimpleTemplate.overrides.update(pydict)
                _chain[-1] = SimpleTemplate.overrides.copy()
            try:
                self.current = next(problem_set_iter[0])
            except StopIteration:
                self.current = None

        def lookup(atpl, to_do=None):
            'Template lookup. This is an extension to bottle SimpleTemplate'
            if atpl in _chain:
                return
            if any([dc['chuery'] == atpl
                for dc in _chain if isinstance(dc, dict)]):
                return
            rsv = resolver(atpl, self.request.chlang)
            _chain.append(atpl)
            if to_do and '.' in atpl:#. -> not for scripts
                to_do(rsv)
            else:
                rsv.stplpath = langlookup(atpl)
            if not rsv.stplpath and re_id.match(atpl):
                raise HTTPError(404, '404_8 ✘ '+atpl)
            yield rsv.stplpath
            del _chain[-1]
            if _chain and isinstance(_chain[-1], dict):
                SimpleTemplate.overrides = _chain[-1].copy()

        if tplid and isinstance(tplid, str) or self.problem:
            def prebase(to_do):
                'template creation for either _new or _zip'
                del _chain[:]
                env.clear()
                env.update({'chripts': {}})
                cleanup = None
                if '\n' in tplid:
                    cleanup = lookup(self.query_show, to_do)
                    try: next(cleanup)
                    except StopIteration:pass
                tpl = get_tpl(tplid,
                    template_lookup=lambda n: lookup(n, to_do))
                try:
                    tpl.execute(stdout,env)
                except AttributeError:
                    c = self.current or self.problem
                    if c:
                        #logger.info('data does not fit to template ' + str(c.chiven))
                        db.delete_keys([c.key])
                    raise
                if cleanup:
                    try: next(cleanup)
                    except StopIteration:pass

            if not self.problem:
                prebase(_new)
            else:
                if len(self.problem_set):
                    self.problem_set = db.problem_set(self.problem)
                problem_set_iter[0] = iter(self.problem_set)
                self.current = self.problem
                try:
                    prebase(_zip)
                except HTTPError:
                    # database entry is out-dated
                    db.del_collection(self.problem)
                    self.problem = None
                    prebase(_new)
            chontent = ''.join(stdout)
        else:
            try:
                urlopt = tuple(tplid)
            except:
                urlopt = tuple()
            chontent = db.filtered_index(self.request.chlang, urlopt)

        if rebase:
            SimpleTemplate.overrides = {}
            del stdout[:]  # the script functions will write into this
            tpl = get_tpl(layout, template_lookup=langlookup)
            choblemkey = self.problem and db.urlsafe(self.problem.key)
            choblems = next(problems_cntr) > 0
            env.update(
                dict(
                    chontent=chontent,
                    chummary=(
                        withempty,
                        noempty),
                    choblem=self.problem,
                    choblemkey=choblemkey,
                    choblems=choblems,
                    ))
            tpl.execute(stdout, env)
            return ''.join(stdout)
        else:
            return chontent

    def tpl_from_qs(self):
        qs = self.query_show

        #qs='r.a&r.b=1'
        name_val = parse_qsl(qs, True)

        if set(''.join(x+y for x,y in name_val))&codemarkers:
            raise HTTPError(400,'400_9')

        if not name_val:
            return name_val

        indexquery = [(qa, qb) for qa, qb in name_val if qa in
                ['level','kind','path','link']]
        if indexquery:
            return indexquery

        ## ignore top level entries in query
        # name_val=[('a','2'),('b.c','')]
        name_val = [(qa,qb) for qa,qb in name_val if '.' in qa]

        cnt = len(name_val)
        if cnt == 0:
            return
        if cnt == 1 and len(name_val[0]) == 2 and name_val[0][1]:
            try:
                cnt = int(name_val[0][1])
            except ValueError:
                pass
        if cnt > 1:
            tpllns = ["%globals().update(include('chcko/chelper',withnr=get('withnr',False)))"]
            inr = count()
            for prob, istr in name_val:
                if not istr:
                    ii = 1
                else:
                    try:
                        ii = int(istr)
                    except ValueError:
                        ii = 1
                for _ in range(ii):
                    chumber = next(inr)+1
                    tpllns.append(f"%chinc('{prob}',{chumber})")
            return '\n'.join(tpllns)
        else:
            return name_val[0][0]

    def get_response(self,**kextra):
        self._get_problem()
        res = self.load_content()
        return res

    def check_answers(self, problem):
        rsv = resolver(problem.chuery, problem.chlang)
        d = rsv.load()
        problem.chanswered = datetime.datetime.now()
        if problem.chesults:
            indict = {q:self.request.forms.get(q,'') for q in self.request.forms.keys()
                 if any(q.startswith(x) for x in problem.chinputids)}
            fromindict = lambda q: indict[q] if q in indict else ''.join([
                    k.split('_')[-1] for k,v in indict.items() if k.startswith(q+'_') and v != '0'])
            answ = [fromindict(q) for q in problem.chinputids]
            db.set_answer(problem,answ)
            na = d.chorm(problem.chanswers)
            problem.choks = d.chequal(na, problem.chesults)
        db.save(problem)

    def post_response(self):
        'answers a POST request'
        choblemkey = self.request.forms.get('choblemkey','') or (
            self.problem and db.urlsafe(self.problem.key))
        self._get_problem(choblemkey)
        if self.problem and not self.problem.chanswered:
            withempty, noempty = Page.make_summary()
            for p in self.problem_set:
                self.check_answers(p)
                sw, sn = self.make_summary(p)
                withempty.__iadd__(sw)
                noempty.__iadd__(sn)
            if withempty.counted > 0:
                db.set_answer(self.problem,[Util.summary(withempty, noempty)])
                # else cleaning empty answers would remove this
            self.check_answers(self.problem)
        return self.load_content()

    @staticmethod
    def make_summary(p=None):
        def smry(f):
            'used to increment a summary'
            try:
                nq = len(f(p.chinputids))
                foks = f(p.choks or [False] * nq)
                fpoints = f(p.choints)
                cnt = 1
            except:
                cnt, nq, foks, fpoints = 0, 0, [], []
            return Struct(counted=cnt,
                          choks=sum(foks),
                          chof=len(foks),
                          choints=sum([foks[i] * fpoints[i] for i in range(nq)]),
                          challpoints=sum(fpoints))
        return (smry(lambda c: c),
            smry(lambda c: [cc for i, cc in enumerate(c) if p.chanswers[i]]))


# course

nokey = lambda x: re.sub('key=[^&]+&','',x)

def course_labels(qs):
    """
    >>> qs = 'a.x&&b.y&&&c.z=1'
    >>> course_labels(qs)
    ['1', '2', '3', '1', '3']
    >>> qs = 'a.x&&b.y&&c.z'
    >>> course_labels(qs)
    ['1', '3', '1', '2', '3']
    >>> qs = 'a.x&b.y&c.z'
    >>> course_labels(qs)
    >>> qs = '&&a.x&b.y&c.z'
    >>> course_labels(qs)
    >>> qs = 'a.x&&&b.y&c.z&&&'
    >>> course_labels(qs)
    ['1', '1', '2', '1', '2']
    >>> qs = 'a.x&&&&b.y&c.z'
    >>> course_labels(qs)
    ['1', '2', '1', '2', '2']
    >>> qs = 'a.x'
    >>> course_labels(qs)
    >>> qs = ''
    >>> course_labels(qs)

    """
    if '&&' in qs:
        qs = [x for x in qs.strip('&').split('&&') if x]
        end = len(qs)
        if end > 1:
            try:
                pos = next(i for i,x in enumerate(qs) if x[0]=='&')
            except StopIteration:
                pos = 0
            b0 = 0,(pos-1)%end,pos,(pos+1)%end,end-1
            return [str(b+1) for b in b0]



def show_qs(qs):
    """
    >>> qs = 'a.x&&b.y&&&c.z=1'
    >>> show_qs(qs)
    'c.z'
    >>> qs = 'a.x&&b.y&&c.z'
    >>> show_qs(qs)
    'a.x'
    >>> qs = 'a.x&b.y&c.z'
    >>> show_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = '&&a.x&b.y&c.z'
    >>> show_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = 'a.x&&&b.y&c.z&&&'
    >>> show_qs(qs)
    'b.y&c.z'
    >>> qs = 'a.x&&&&b.y&c.z'
    >>> show_qs(qs)
    'a.x'
    >>> qs = 'a.x'
    >>> show_qs(qs)
    'a.x'
    >>> qs = ''
    >>> show_qs(qs)
    ''

    """
    if '&&' in qs:
        qs = [x for x in qs.strip('&').split('&&') if x]
        try:
            qs = next(filter(lambda x:x[0]=='&',qs))
        except StopIteration:
            qs = qs[0]
        qs = qs.strip('&')
        if qs.endswith('=1'):
            qs = qs[:-2]
    return qs

def next_qs(qs,direction=1):
    """
    >>> qs = 'a.x&&b.y&&&c.z'
    >>> next_qs(qs)
    'a.x&&b.y&&c.z'
    >>> qs = 'a.x&&b.y&&c.z'
    >>> next_qs(qs)
    'a.x&&&b.y&&c.z'
    >>> qs = 'a.x&b.y&c.z'
    >>> next_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = '&&a.x&b.y&c.z'
    >>> next_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = 'a.x&&&b.y&c.z&&&'
    >>> next_qs(qs)
    'a.x&&b.y&c.z'
    >>> qs = 'a.x&&&&b.y&c.z'
    >>> next_qs(qs)
    'a.x&&&b.y&c.z'
    >>> qs = 'a.x&&&b.y&&c.z'
    >>> next_qs(qs)
    'a.x&&b.y&&&c.z'
    >>> qs = 'a.x'
    >>> next_qs(qs)
    'a.x'
    >>> qs = ''
    >>> next_qs(qs)
    ''
    >>> qs = 'a.x&&b.y&&&c.z'
    >>> next_qs(qs,-1)
    'a.x&&&b.y&&c.z'
    >>> qs = 'a.x&&b.y&&c.z'
    >>> next_qs(qs,-1)
    'a.x&&b.y&&&c.z'
    >>> qs = 'a.x&b.y&c.z'
    >>> next_qs(qs,-1)
    'a.x&b.y&c.z'
    >>> qs = '&&a.x&b.y&c.z'
    >>> next_qs(qs,-1)
    'a.x&b.y&c.z'
    >>> qs = 'a.x&&&b.y&c.z&&&'
    >>> next_qs(qs,-1)
    'a.x&&b.y&c.z'
    >>> qs = 'a.x&&&&b.y&c.z'
    >>> next_qs(qs,-1)
    'a.x&&&b.y&c.z'
    >>> qs = 'a.x&&b.y&&&c.z'
    >>> next_qs(qs,-1)
    'a.x&&&b.y&&c.z'
    >>> qs = 'a.x'
    >>> next_qs(qs,-1)
    'a.x'
    >>> qs = ''
    >>> next_qs(qs,-1)
    ''

    """
    if '&&' in qs:
        qs = [x for x in qs.strip('&').split('&&') if x]
        qslen = len(qs)
        try:
            qi,_ = next(filter(lambda x:x[1][0]=='&',enumerate(qs)))
        except StopIteration:
            qi = 0
        qs = [q.strip('&') for q in qs]
        qi = (qi+direction) % qslen
        if qi >= 0 and qi < qslen:
            qs[qi] = '&'+qs[qi]
        qs = '&&'.join(qs)
    return nokey(qs.strip('&'))

def start_qs(qs):
    """
    >>> qs = 'a.x&&b.y&&&c.z'
    >>> start_qs(qs)
    'a.x&&b.y&&c.z'
    >>> qs = 'a.x&b.y&c.z'
    >>> start_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = ''
    >>> start_qs(qs)
    ''

    """
    return nokey('&&'.join([x.strip('&') for x in qs.strip('&').split('&&') if x]))

def end_qs(qs):
    """
    >>> qs = 'a.x&&b.y&&c.z'
    >>> end_qs(qs)
    'a.x&&b.y&&&c.z'
    >>> qs = 'a.x&b.y&c.z'
    >>> end_qs(qs)
    'a.x&b.y&c.z'
    >>> qs = ''
    >>> end_qs(qs)
    ''

    """
    try:
        qss = [x.strip('&') for x in qs.strip('&').split('&&') if x]
        res = '&&'.join(qss[:-1]+['&'+qss[-1]])
    except:
        res = ''
    return nokey(res.strip('&'))

