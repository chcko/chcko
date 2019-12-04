# -*- coding: utf-8 -*-
from random import randrange
from math import log
from chcko.hlp import Struct


def given():
    g = Struct()
    g.Kn = randrange(1000, 2000)
    g.R = randrange(100, 200)
    g.i = randrange(2, 9)
    return g


def calc(g):
    r = log(g.Kn * g.i / 100.0 / g.R + 1) / log(1.0 + g.i / 100.0)
    return [r]
