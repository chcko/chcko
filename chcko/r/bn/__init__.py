# -*- coding: utf-8 -*-
from random import randrange
from math import log
from chcko.hlp import Struct


def given():
    g = Struct()
    g.Kn = randrange(1000, 2000)
    g.K0 = randrange(20, 999)
    g.i = randrange(2, 9)
    return g


def calc(g):
    res = log(g.Kn / g.K0) / log(1.0 + g.i / 100.0)
    return [res]
