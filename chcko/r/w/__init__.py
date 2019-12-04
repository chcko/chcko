# -*- coding: utf-8 -*-

import random

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
    g = Struct(b=b, e=e)
    return g


def calc(g):
    x = 1.0 * g.b ** (1.0 * g.e)
    return [x]
