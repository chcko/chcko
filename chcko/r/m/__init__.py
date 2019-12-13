# -*- coding: utf-8 -*-
import random
import numpy as np
from chcko.hlp import Struct, norm_int as norm


def given():
    g = Struct()
    g.i = random.sample(range(2, 12), 1)[0]
    g.K1 = random.sample(range(30, 50), 1)[0] * 1000
    g.n1, g.n2 = random.sample(range(1, 20), 2)
    dK = random.sample(list(range(-50, -1)) + list(range(1, 50)), 1)[0] * 10
    g.K2 = int(g.K1 * (1.0 + g.i / 100.0) ** (g.n2 - g.n1) + dK)
    return g


def calc(g):
    # g=Struct(i=8,K1=47000,n1=18,K2=36940,n2=15)
    res = 2 if g.K1 * (1.0 + g.i / 100.0) ** (g.n2 - g.n1) < g.K2 else 1
    return [res]
