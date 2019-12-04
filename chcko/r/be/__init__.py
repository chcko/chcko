# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct, listable


def given():
    g = Struct()
    g.i = randrange(20, 256)
    return g


@listable
def norm(a):
    return a.lstrip('0')


def calc(g):
    return ['{0:b}'.format(g.i)]
