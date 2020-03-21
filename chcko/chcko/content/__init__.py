# -*- coding: utf-8 -*-
"""
The content page is the default, if no page specified.

With content IDs::

    /<lang>/[content][?(<author>.<id>[=<cnt>])&...]

    /en/?r.a=2&r.bu

Without content IDs it is an index page, which can be filter::

    /<lang>/content[?<filter>=<value>&...]

    /en/content?level=10&kind=1&path=maths&link=r

See ``filtered_index`` for that.

"""

import re
import datetime

from urllib.parse import parse_qsl
from chcko.chcko.bottle import SimpleTemplate, StplParser, get_tpl, HTTPError
from chcko.chcko.hlp import (
        Struct,
        resolver,
        mklookup,
        counter,
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
        self.query_string = self.request.query_string.replace(';','&')
        self.query_show = show_qs(self.query_string)

    def _get_problem(self, problemkey=None):
        '''init the problem from database if it exists
        '''
        urlsafe = problemkey or self.query_string.startswith(
            'key=') and self.query_string[4:]

        if urlsafe:
            self.problem = db.from_urlsafe(urlsafe)
            if self.problem:  # else it was deleted
                if not isinstance(self.problem,db.Problem):
                    raise HTTPError(404, "No such problem")
                # query_string here is "key=..."
                # replace query_show/query_string with that of the problem to load the problem in tpl_from_qs()
                self.query_show = self.problem.query_string
        else:  # get existing unanswered if query_string is same
            self.problem = db.problem_by_query_string(
                self.query_show,
                self.request.lang,
                self.request.student)

        if self.problem:
            keyOK = self.problem.key.parent()
            while keyOK and keyOK.get().userkey != self.request.student.userkey:
                keyOK = keyOK.parent()
            if not keyOK:
                logger.warning(
                    "%s not for %s", db.urlstring(self.problem.key), db.urlstring(self.request.student.key))
                raise HTTPError(400,'no permission')
            self.problem_set = db.problem_set(self.problem)
        elif problemkey is None:  # XXX: Make deleting empty a cron job
            # remove unanswered problems for this user
            # timedelta to have the same problem after returning from a
            # followed link
            age = datetime.datetime.now() - datetime.timedelta(days=1)
            db.del_stale_open_problems(self.request.student,age)

    def load_content(self
                     , layout='chcko/content'
                     , rebase=True
                     ):
        ''' evaluates the templates with includes therein and zips them to database entries

        examples:
            chcko/chcko/tests/test_content.py

        '''

        tplid = self.tpl_from_qs()
        _chain = []
        withempty, noempty = self.make_summary()
        nrs = counter()
        problems_cntr = counter()
        SimpleTemplate.overrides = {}
        problem_set_iter = [None]
        langlookup = mklookup(self.request.lang)

        def _new(rsv):
            nr = next(nrs)
            problem, from_py = db.problem_from_resolver(
                rsv, nr, self.request.student)
            if not self.problem:
                self.problem = problem
                self.current = self.problem
            else:
                db.add_to_set(problem,self.problem)
            if problem.points:
                next(problems_cntr)
            db.save(problem)
            if not rsv.composed:
                SimpleTemplate.overrides.update(from_py)
                _chain[-1] = SimpleTemplate.overrides.copy()

        def _zip(rsv):
            if not self.current or rsv.query_string != self.current.query_string:
                ms = 'query string ' + rsv.query_string
                ms += ' not in sync with database '
                if self.current:
                    ms += self.current.query_string
                logger.info(ms)
                raise HTTPError(400,ms)
            from_py = rsv.load()  # for the things not stored, like 'names'
            from_py.update(db.fieldsof(self.current))
            from_py.update({
                'lang': self.request.lang,
                'g': self.current.given,
                'request': self.request})
            if self.current.points:
                next(problems_cntr)
            if self.current.answered:
                sw, sn = self.make_summary(self.current)
                from_py.update({'summary': (sw, sn)})
                withempty.__iadd__(sw)
                noempty.__iadd__(sn)
            if not rsv.composed:
                SimpleTemplate.overrides.update(from_py)
                _chain[-1] = SimpleTemplate.overrides.copy()
            try:
                self.current = next(problem_set_iter[0])
            except StopIteration:
                self.current = None

        def lookup(atpl, to_do=None):
            'Template lookup. This is an extension to bottle SimpleTemplate'
            if atpl in _chain:
                return
            if any([dc['query_string'] == atpl
                for dc in _chain if isinstance(dc, dict)]):
                return
            rsv = resolver(atpl, self.request.lang)
            _chain.append(atpl)
            if to_do and '.' in atpl:#. -> not for scripts
                to_do(rsv)
            else:
                rsv.templatename = langlookup(atpl)
            if not rsv.templatename and re_id.match(atpl):
                raise HTTPError(404, '✘ '+atpl)
            yield rsv.templatename
            del _chain[-1]
            if _chain and isinstance(_chain[-1], dict):
                SimpleTemplate.overrides = _chain[-1].copy()

        env = {}
        stdout = []

        if tplid and isinstance(tplid, str) or self.problem:
            def prebase(to_do):
                'template creation for either _new or _zip'
                del _chain[:]
                env.clear()
                env.update({
                    'query_string': self.query_string,
                    'lang': self.request.lang,
                    'scripts': {}})
                cleanup = None
                if '\n' in tplid:
                    cleanup = lookup(self.query_show, to_do)
                    try: next(cleanup)
                    except StopIteration:pass
                tpl = get_tpl(
                    tplid,
                    template_lookup=lambda n: lookup(n, to_do))
                try:
                    tpl.execute(stdout, env)
                except AttributeError:
                    c = self.current or self.problem
                    if c:
                        logger.info('data does not fit to template ' + str(c.given))
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
            content = ''.join(stdout)
        else:
            content = db.filtered_index(self.request.lang, tplid)

        nrs.close()

        if rebase:
            SimpleTemplate.overrides = {}
            del stdout[:]  # the script functions will write into this
            tpl = get_tpl(layout, template_lookup=langlookup)
            problemurlsafe = self.problem and db.urlsafe(self.problem.key)
            with_problems = next(problems_cntr) > 0
            env.update(
                dict(
                    content=content,
                    summary=(
                        withempty,
                        noempty),
                    problem=self.problem,
                    problemkey=problemurlsafe,
                    with_problems=with_problems,
                    request=self.request))
            tpl.execute(stdout, env)
            problems_cntr.close()
            return ''.join(stdout)
        else:
            return content

    def tpl_from_qs(self):
        qs = self.query_show

        qparsed = parse_qsl(qs, True)

        if set(''.join(x+y for x,y in qparsed))&codemarkers:
            raise HTTPError(400,'Wrong characters in query.')

        if not qparsed:
            return qparsed

        indexquery = [(qa, qb) for qa, qb in qparsed if qa in
                ['level','kind','path','link']]
        if indexquery:
            return indexquery

        ## ignore top level entries in query
        # qparsed=[('a',2),('b.c',3)]
        qparsed = [(qa,qb) for qa,qb in qparsed if '.' in qa]

        cnt = len(qparsed)
        if cnt == 0:
            return
        if (cnt > 1 or
                (cnt == 1 and
                 len(qparsed[0]) == 2 and
                 qparsed[0][1] and
                 int(qparsed[0][1]) > 1)):
            res = []
            icnt = counter()
            for q, i in qparsed:
                if not i:
                    i = '1'
                try:
                    ii = int(i)
                except ValueError:
                    ii = 1
                for _ in range(ii):
                    res.append(Util.inc(q, icnt))
            return '\n'.join(res)
        else:
            return qparsed[0][0]

    def get_response(self):
        self._get_problem()
        res = self.load_content()
        return res

    def check_answers(self, problem):
        rsv = resolver(problem.query_string, problem.lang)
        d = rsv.load()
        problem.answered = datetime.datetime.now()
        if problem.results:
            db.set_answer(problem,[self.request.forms.get(q,'') for q in problem.inputids])
            na = d.norm(problem.answers)
            problem.oks = d.equal(na, problem.results)
        db.save(problem)

    def post_response(self):
        'answers a POST request'
        problemkey = self.request.forms.get('problemkey','') or (
            self.problem and db.urlsafe(self.problem.key))
        self._get_problem(problemkey)
        if self.problem and not self.problem.answered:
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
                nq = len(f(p.inputids))
                foks = f(p.oks or [False] * nq)
                fpoints = f(p.points)
                cnt = 1
            except:
                cnt, nq, foks, fpoints = 0, 0, [], []
            return Struct(counted=cnt,
                          oks=sum(foks),
                          of=len(foks),
                          points=sum([foks[i] * fpoints[i] for i in range(nq)]),
                          allpoints=sum(fpoints))
        return (smry(lambda c: c),
            smry(lambda c: [cc for i, cc in enumerate(c) if p.answers[i]]))


# course

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
    return qs.strip('&')

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
    return '&&'.join([x.strip('&') for x in qs.strip('&').split('&&') if x])

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
    return res.strip('&')

