# -*- coding: utf-8 -*-
'''

Utility

'''

from sympy.parsing.sympy_parser import parse_expr
from sympy import Poly, latex
from sympy.abc import x
from urllib.parse import parse_qsl
import logging

from bottle import SimpleTemplate, template

from chcko.hlp import listable, mklookup, counter, Struct
from chcko.languages import langkindnum, langnumkind, CtxStrings
from chcko.model import studentCtx, Student


class Util:
    ''' A Util instance named ``util`` is available in html files.
    '''

    def __init__(self, request):
        self.request = request

    def query(self):
        return [
            d[0] if not d[1] else d for d in parse_qsl(
                self.request.query_string,
                True)]

    def a(self, lnk):
        return '<a href="/' + self.request.lang + \
            '/?' + lnk + '">' + lnk + '</a>'

    def newlang(self, lng):
        np = self.request.path_qs.replace(
            '/' +
            self.request.lang,
            '/' +
            lng,
            1)
        return '<a href="' + np + '">' + lng + '</a>'

    @staticmethod
    def inc(lnk, cntr=counter(), stack=[]):
        n = next(cntr) + 1
        nn = '/'.join([str(n)] + stack + [lnk])
        res = []
        res.append('''<div class="subproblem{}">
            <span class="problem_id">{} )</span>'''.format((n - 1) % 2, nn))
        res.append("% include('" + lnk + "')")
        res.append('</div>')
        return '\n'.join(res)

    def translate(self, word):
        try:
            idx = studentCtx.index(word)
            res = CtxStrings[self.request.lang][idx]
            return res
        except:
            return word

    @staticmethod
    def user_path(skey, user):
        anc = [(skey, skey.get().userkey == (user and user.key))]
        parent = skey.parent()
        while parent:
            anc = [(parent, parent.get().userkey == (user and user.key))] + anc
            parent = parent.parent()
        return anc

    @staticmethod
    def all_of(user):
        students = Student.query(
            Student.userkey == user.key).iter(
            keys_only=True)
        for skey in students:
            yield Util.user_path(skey, user)

    @staticmethod
    def summary(withempty, noempty):
        sf = "{oks}/{of}->{points}/{allpoints}"
        s = sf.format(**withempty) + "  \\Ø:" + sf.format(**noempty)
        return s

    @staticmethod
    def tex(term):
        try:
            e = parse_expr(term)
        except:
            e = term
        ltx = latex(e)
        return ltx

    @staticmethod
    def tex_poly(gc, domain='ZZ'):
        p = Poly(gc, x, domain='ZZ')
        ltx = latex(p.as_expr())
        return ltx

    @staticmethod
    def tx(fun):
        return lambda term: r'\(' + fun(term) + r'\)'

    @staticmethod
    def Tx(fun):
        return lambda term: r'\[' + fun(term) + r'\]'

    @staticmethod
    def J(*args):
        return ''.join([str(x) for x in args])

    @staticmethod
    def sgn(v):
        if v >= 0:
            return '+'
        else:
            return '-'

    @staticmethod
    @listable
    def F(*args):
        ''' format based on first argument
        >>> Util.F(["S{0} = "],[1,2,3])
        ['S1 = ', 'S2 = ', 'S3 = ']

        '''
        f = args[0]
        return f.format(*args[1:])


class PageBase:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user
        self.util = Util(self.request)
        SimpleTemplate.defaults.update(self.request.params)
        SimpleTemplate.defaults.update({
            'session': self.session,
            'request': self.request,
            'user': self.user,
            'util': self.util,
            'kinda': langkindnum[self.request.lang],
            'numkind': langnumkind[self.request.lang],
            'langs': list(CtxStrings.keys())
        })
        self.params = self.request.params
    def set_user(email,password):
        self.user = self.request.user = User.get_by_login(email,password)
        set_student(self.request,self.user,self.session)
    def get_response(self):
        return template(
            self.request.pagename,
            self.params,
            template_lookup=mklookup(
                self.request.lang))
    def redirect(self, afterlang):
        return bottle.redirect('/{}/{}'.format(self.request.lang,afterlang))

def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect('login')
        else:
            return handler(self, *args, **kwargs)
    return check_login



# mathml not used currently
#
# from sympy.printing import mathml
# from sympy.utilities.mathml import c2p
# from lxml import etree
#
# def pmathml(expr):
#     '''
#     >>> from sympy.abc import x
#     >>> expr=x**2+x
#     >>> [ln.strip() for ln in pmathml(expr).splitlines()][2:-3]
#     [u'<msup>', u'<mi>x</mi>', u'<mn>2</mn>', u'</msup>']
#
#     '''
# trx = c2p(mathml(expr)) #<?xml version=...>\n<math...
# trx = '\n'.join(trx.splitlines()[1:]) #<math...
#     trx = trx.replace('xmlns=','x=')
#     trx = '<root>\n'+trx+'\n</root>'
#     rx = etree.XML(trx)
# etree.strip_tags(rx,'math') #<math with all attributes
#     uc=etree.tounicode(rx)
#     uc=u'\n'.join(uc.splitlines()[1:-1])
#     return uc
