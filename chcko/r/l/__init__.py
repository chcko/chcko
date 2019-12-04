# -*- coding: utf-8 -*-

import random
import numpy as np
from chcko.hlp import Struct, norm_frac as norm


def given():
    r = sorted(random.sample(range(-9, -1) + range(1, 9), 2))
    c = [-1, r[0] + r[1], -r[0] * r[1]]
    g = Struct(r=r, c=c)
    return g


def calc(g):
    p = np.poly1d(g.c)
    p_i = np.polyint(p)
    I = p_i(g.r[1]) - p_i(g.r[0])
    return [I]
