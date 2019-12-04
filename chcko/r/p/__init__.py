# -*- coding: utf-8 -*-

import random
from math import log

from chcko.hlp import Struct, norm_frac as norm

be = []
for i in range(2, 5):
    for j in range(-4, 5):
        be.append((i, j))
for i in range(2, 5):
    for j in range(-4, 5):
        be.append((1.0 / i, j))
random.shuffle(be)


def given():
    b, e = random.sample(be, 1)[0]
    n = 1.0 * b ** (1.0 * e)
    g = Struct(b=b, n=n)
    return g


def calc(g):
    res = 1.0 * log(g.n) / log(g.b)
    return [res]
