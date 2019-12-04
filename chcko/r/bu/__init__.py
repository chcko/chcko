# -*- coding: utf-8 -*-
from random import sample
from chcko.hlp import Struct, norm_int as norm


def given():
    a, c = sample(range(2, 9) + range(-9, -2), 2)
    x = sample(range(2, 9) + range(-9, -2), 1)[0]
    b = (c - a) * x
    g = Struct(a=a, b=b, c=c)
    return g


def calc(g):
    res = g.b / (g.c - g.a)
    return [res]
