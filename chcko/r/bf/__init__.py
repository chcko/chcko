# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct, listable


def given():
    g = Struct()
    g.a = randrange(20, 128)
    g.b = randrange(20, 128)
    return g


@listable
def norm(a):
    return a.lstrip('0')


def calc(g):
    return ['{0:b}'.format(g.a + g.b)]
