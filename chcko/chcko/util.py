# -*- coding: utf-8 -*-
'''

Utility

'''

from sympy.parsing.sympy_parser import parse_expr
from sympy import Poly, latex
from sympy.abc import x
from urllib.parse import parse_qsl
from itertools import count

from chcko.chcko import bottle
from chcko.chcko.bottle import SimpleTemplate, template

from chcko.chcko.hlp import listable, mklookup
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
                True) if d[0] not in db.pathlevels]

    def a(self, alnk):
        return """<a href="#" onclick="a_lnk('"""+alnk+"""');return false;">"""+alnk+'</a>'

    def newlang(self, lng):
        oldp = self.request.urlparts.path.strip('/')
        try:
            curlng = next(l for l in langs if oldp==l or oldp.startswith(l+'/'))
        except StopIteration:
            curlng = ''
        if curlng:
            newp = oldp.replace(curlng,lng,1)
        else:
            newp = lng+'/'+oldp
        newlnk = newurl('/'+newp)
        return '<a href="' + newlnk + '">' + lng + '</a>'

    def translate(self, word):
        try:
            idx = db.pathlevels.index(word)
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
    def TX(term):
        if isinstance(term,list):
            e = Poly(term, x, domain='ZZ').as_expr()
        else:
            try:
                e = parse_expr(term)
            except:
                e = term
        ltx = latex(e)
        return ltx

    @staticmethod
    def tx(term):
       return r'\('+Util.TX(term)+r'\)'

    @staticmethod
    def Tx(term):
        return r'\['+Util.TX(term)+r'\]'

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
        SimpleTemplate.defaults.clear()
        SimpleTemplate.defaults['rolecolor'] = self.request.student.color
        SimpleTemplate.defaults.update(mod.__dict__)
        SimpleTemplate.defaults.update({
            'self': self,
            'util': self.util,
            'langs': langs,
            'db': db,
            'social_logins': social_logins,
            #as default if no problem ...
            'query_string': self.request.query_string,
            'lang': self.request.lang,
        })
        try:
            SimpleTemplate.defaults.update({
                'kinda': langkindnum[self.request.lang],
                'numkind': langnumkind[self.request.lang]
            })
        except:
            pass
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
