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
    g = Struct(bn=bn, bd=bd, en=en, ed=ed)
    return g


def calc(g):
    nm = 1
    for i, ae in enumerate(g.en):
        nm = nm * simplify(g.bn[i]) ** ae
    for i, ae in enumerate(g.ed):
        nm = nm / simplify(g.bd[i]) ** ae
    return [sstr(simplify(nm))]

norm = lambda x: x
