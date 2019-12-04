# -*- coding: utf-8 -*-

import re
import datetime
import logging

from urlparse import parse_qsl
from chcko.model import depth_1st, problemCtxObjs, keysOmit, table_entry, ctxkey
from chcko.hlp import datefmt, last
from chcko.util import PageBase
from google.appengine.ext import ndb


def prepare(
        qs  # url query_string (after ?)
        , skey  # start key, filter is filled up with it.
    # student key normally, but can be other, e.g. school, too.
        # if a parent belongs to user then all children can be queried
        , userkey
):
    '''prepares the perameters for depth_1st

    >>> #see depth_1st
    >>> skey = ctxkey(['Sc1', 'Pe1', 'Te1','Cl1','St1'])
    >>> #qs= "Sc0&*&*&*&*&*"
    >>> qs= "q~r.be"
    >>> prepare(qs,skey,None)[0]
    ['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1', [('query_string', '=', 'r.be')]]
    >>> qs= '  '
    >>> prepare(qs,skey,None)[0]
    ['Sc1', 'Pe1', 'Te1', 'Cl1', 'St1', []]
    >>> qs= "1DK&*&d>3"
    >>> p = prepare(qs,skey,None)[0]

    '''
    @last
    def filters(x):
        '''convert to GAE filters from
        lst is ["<field><operator><value>",...]
        ~ -> =
        q = query_string
        age fields: H = hours, S = seconds, M = minutes, d = days

        '''
        AGES = {'d': 'days', 'H': 'hours', 'M': 'minutes', 'S': 'seconds'}
        ABBR = {'q': 'query_string'}
        filters = []
        if not isinstance(x, str):
            return
        for le in x.split(','):
            #le = next(iter(x.split(',')))
            le = le.replace('~', '=')
            match = re.match(r'(\w+)([=!<>]+)([\w\d\.]+)', le)
            if match:
                grps = match.groups()
                name, op, value = grps
                if name in ABBR:
                    name = ABBR[name]
                age = None
                # le='d<~3'
                if name in AGES:
                    age = AGES[name]
                if name in AGES.values():
                    age = name
                if age:
                    value = datetime.datetime.now(
                    ) - datetime.timedelta(**{age: int(value)})
                    name = 'answered'
                filters.append((name, op, value))
        return filters
    #qs = ''
    O = problemCtxObjs
    # q=query, qq=*->[], qqf=filter->gae filter (name,op,value)
    q = filter(None, [k.strip() for k, v in parse_qsl(qs, True)])
    qq = [[] if x == '*' else x for x in q]
    qqf = [filters() if filters(x) else x for x in qq]
    # fill up to len(O)
    delta = len(O) - len(qqf)
    if delta > 0:
        ext = [str(v) for k, v in skey.pairs()]
        extpart = min(len(ext), delta)
        rest = delta - extpart
        qqf = ext[:extpart] + [[]] * rest + qqf
    keys = keysOmit(qqf)
    obj = keys and keys[-1].get()  # parent to start from
    if obj and obj.userkey == userkey:
        return qqf, keys, O, True
    else:
        return qqf, [], O, False, userkey


class Page(PageBase):

    def __init__(self, _request):
        super(self.__class__, self).__init__(_request)
        self.table = lambda: depth_1st(
            *
            prepare(
                self.request.query_string,
                self.request.student.key,
                self.user and self.user.key))
        self.params = {
            'table': self.table,
            'table_entry': table_entry}

    def post_response(self):
        for urlsafe in self.request.get_all('deletee'):
            k = ndb.Key(urlsafe=urlsafe)
            k.delete()
        return self.get_response()
