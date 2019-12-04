# -*- coding: utf-8 -*-

import random

from chcko.hlp import Struct


def given():
    r, s = random.sample(range(1, 9), 2)
    m = random.sample(range(18, 21), 1)[0]
    u = random.sample(range(700, 900), 1)[0]
    g = random.sample(range(30, 50), 1)[0]
    e = 1.0 * u / (1 + g / 100.0)
    v = 1.0 * u * (1 - r / 100.0) * (1 - s / 100.0) * (1 + m / 100.0)
    g = Struct(r=r, s=s, m=m, v=v, e=e)
    return g


def calc(g):
    u = g.v / (1 - g.r / 100.0) / (1 - g.s / 100.0) / (1 + g.m / 100.0)
    n = 100.0 * (u - g.e) / g.e
    return [u, n]
