# -*- coding: utf-8 -*-

from chcko.hlp import Struct, norm_frac as norm
import random
from sympy import Rational as R

__all__ = ['given', 'calc']


def given():
    g = Struct()
    g.x = random.sample(range(-9, -1) + range(1, 9), 2)
    g.b = random.sample(range(-9, -1) + range(1, 9), 1)[0]
    return g


def calc(g):
    res = [R(g.b, g.x[1])]
    return res
