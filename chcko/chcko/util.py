# -*- coding: utf-8 -*-
'''

Utility

'''

from sympy.parsing.sympy_parser import parse_expr
from sympy import Poly, latex
from sympy.abc import x
from urllib.parse import parse_qsl

from chcko.chcko import bottle
from chcko.chcko.bottle import SimpleTemplate, template

from chcko.chcko.hlp import listable, mklookup, counter, logger, from_py
from chcko.chcko.languages import langkindnum, langnumkind, role_strings
from chcko.chcko.db import db

from chcko.chcko.auth import newurl

try:
    from chcko.chcko.auth import social_logins
except:
    social_logins = {}

langs = list(role_strings.keys())

class Util:
    ''' A Util instance named ``util`` is available in html files.
    '''

    def __init__(self, request):
        self.request = request

    def parsedquerystring(self):
        return [
            d[0] if not d[1] else d for d in parse_qsl(
                self.request.query_string,
                True) if d[0] not in db.studentplaces]

    def a(self, alnk):
        return '<a href="#" onclick="a_content('+alnk+');return false;">'+alnk+'</a>'

    def newlang(self, lng):
        oldp = self.request.urlparts.path.strip('/')
        try:
            curlng = next(x for x in langs if oldp==x or oldp.startswith(x+'/'))
        except StopIteration:
            curlng = ''
        if curlng:
            newp = oldp.replace(curlng,lng,1)
        else:
            newp = lng+'/'+oldp
        newlnk = newurl('/'+newp)
        return '<a href="' + newlnk + '">' + lng + '</a>'

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
            idx = db.studentplaces.index(word)
            res = role_strings[self.request.lang][idx]
            return res
        except:
            return word

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
    def __init__(self,mod):
        self.request = bottle.request
        self.response = bottle.response
        self.util = Util(self.request)
        SimpleTemplate.defaults.update(self.request.params)
        SimpleTemplate.defaults.update(from_py(mod))
        SimpleTemplate.defaults.update({
            'self': self,
            'request': self.request,
            'response': self.response,
            'util': self.util,
            'kinda': langkindnum[self.request.lang],
            'numkind': langnumkind[self.request.lang],
            'langs': langs,
            'db': db,
            'logger': logger,
            'social_logins': social_logins,
        })
    def get_response(self):
        res = template('chcko.'+self.request.pagename,**self.request.params,
                template_lookup=mklookup(self.request.lang))
        return res
    def redirect(self, afterlang):
        bottle.redirect(f'/{self.request.lang}/{afterlang}')
    def renew_token(self):
        db.token_delete(self.request.user.token)
        email = db.user_email(self.request.user)
        self.request.user.token = db.token_create(email)
        db.save(self.request.user)
        db.set_cookie('chcko_cookie_usertoken',self.request.user.token)

def user_required(handler):
    def check_login(self, *args, **kwargs):
        if not self.request.user:
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
