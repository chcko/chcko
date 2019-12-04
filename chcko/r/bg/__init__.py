# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct, listable


def given():
    g = Struct()
    g.b = randrange(20, 128)
    g.a = randrange(3, 12) * g.b
    return g


@listable
def norm(a):
    return a.lstrip('0')


def calc(g):
    return ['{0:b}'.format(int(g.a / g.b))]
