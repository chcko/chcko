# -*- coding: utf-8 -*-
import random
from sympy.abc import a, b, c, d, e, f, g, h, i, j, k, m, n, p, q, r, s, t, u, v, w, x, y, z
from sympy import sstr, simplify

from chcko.hlp import Struct, equal_0 as equal

syms = [a, b, c, d, e, f, g, h, i, j, k, m, n, p, q, r, s, t, u, v, w, x, y, z]
syml = 'abcdefghijkmnpqrstuvwxyz'


def given():
    bn = random.sample(syml, 3)
    bd = bn[:]
    random.shuffle(bd)
    en = random.sample(range(-9, 9), 3)
    ed = random.sample(range(-9, 9), 3)
    nm = ''
    for i, ae in enumerate(en):
        nm = nm + '*{0}**{1}'.format(bn[i], ae)
    nm = nm.strip('*')
    dm = ''
    for i, ae in enumerate(ed):
        dm = dm + '*{0}**{1}'.format(bd[i], ae)
    dm = dm.strip('*')
    g = Struct(nm=nm, dm=dm)
    return g


def calc(g):
    return [sstr(simplify(g.nm + '/(' + g.dm + ')'))]

norm = lambda x: x
