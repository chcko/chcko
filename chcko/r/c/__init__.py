# -*- coding: utf-8 -*-
import random
from math import log

from chcko.hlp import Struct


def given():
    g = Struct()
    g.r = random.sample(range(100, 200), 1)[0]
    g.n = random.sample(range(5, 10), 1)[0]
    g.i = random.sample(range(2, 14), 1)[0] / 10.0
    g.m = random.sample(range(2, 7), 1)[0]
    g.m = g.m * 10
    return g


def calc(g):
    q = 1.0 + 1.0 * g.i / 100
    kn = g.r * (1 - q ** g.n) / (1 - q)
    kv = q * kn
    nm = log(g.m * (q - 1) + 1) / log(q)
    ieff = 100 * ((1 + g.i / 100.0) ** 12.0 - 1)
    return [kn, kv, nm, ieff]
