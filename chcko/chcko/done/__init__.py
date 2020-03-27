# -*- coding: utf-8 -*-

import re
import datetime
from urllib.parse import parse_qsl
from chcko.chcko.db import db
from chcko.chcko.util import PageBase
from functools import wraps

def takelast(obj):
    @wraps(obj)
    def memoizer(*args, **kwargs):
        if len(args) + len(kwargs) != 0:
            obj.last = obj(*args, **kwargs)
        return obj.last
    return memoizer


def prepare(
        qs  # url query_string (after ?)
        ,skey  # start key, filter is filled up with it.
               # student key normally, but can be other, e.g. school, too.
               # if a parent belongs to user then all children can be queried
        ,userkey
        ,extraplace = 'Problem'
):
    '''prepares the parameters for db.depth_1st

    >>> from chcko.chcko.db import db
    >>> skey = db.key_from_path(['Sc1', 'Pe1', 'Te1','Cl1','St1'])
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
    @takelast
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
                    name = 'created'
                filters.append((name, op, value))
        return filters
    #qs = ''
    PR = db.pathlevels+[extraplace]
    # q=query, qq=*->[], qqf=filter->gae filter (name,op,value)
    q = filter(None, [k.strip() for k, v in parse_qsl(qs, True) if k not in db.pathlevels])
    qq = [[] if x == '*' else x for x in q]
    qqf = [filters() if filters(x) else x for x in qq]
    # fill up to len(PR)
    delta = len(PR) - len(qqf)
    if delta > 0:
        ext = [str(v) for k, v in skey.pairs()]
        extpart = min(len(ext), delta)
        rest = delta - extpart
        qqf = ext[:extpart] + [[]] * rest + qqf
    keys = db.keys_to_omit(qqf)
    obj = keys and keys[-1].get()  # parent to start from
    if obj and obj.userkey == userkey:
        return qqf, keys, PR, True
    else:
        return qqf, [], PR, False, userkey


class Page(PageBase):

    def __init__(self, mod):
        super().__init__(mod)
        qs = self.request.query_string
        skey = self.request.student.key
        userkey = self.request.user and db.idof(self.request.user)
        self.page_table = lambda: db.depth_1st(*prepare(qs,skey,userkey))

    def post_response(self):
        todelete = []
        for urlsafe in self.request.forms.getall('deletee'):
            todelete.append(db.Key(urlsafe=urlsafe))
        db.delete_keys(todelete)
        return self.get_response()
