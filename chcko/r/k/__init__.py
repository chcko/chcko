# -*- coding: utf-8 -*-
import random
import numpy as np
from chcko.hlp import Struct


def given():
    r = sorted(random.sample(range(-9, -1), 2) + random.sample(range(1, 9), 2))
    c = [-1, +r[0] + r[1] + r[2] + r[3],  # x**4,x**3
         -r[0] * r[1] - r[0] * r[2] - r[0] * r[3] - r[1] *
         r[2] - r[1] * r[3] - r[2] * r[3],  # x**2
         +r[0] * r[1] * r[2] + r[0] * r[1] * r[3] +
         r[0] * r[2] * r[3] + r[1] * r[2] * r[3],  # x
         -r[0] * r[1] * r[2] * r[3]]
    g = Struct(r=r, c=c)
    return g


def calc(g):
    p = np.poly1d(g.c)
    p_i = np.polyint(p)
    I = +p_i(g.r[1]) - p_i(g.r[0]) - p_i(g.r[2]) + \
        p_i(g.r[1]) + p_i(g.r[3]) - p_i(g.r[2])
    return [I]
