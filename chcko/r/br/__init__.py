# -*- coding: utf-8 -*-
from random import sample
from chcko.hlp import Struct, norm_expr as norm

import sympy
from sympy import S, Rational as R
from sympy.abc import x


def given():
    n, d = 2, -2
    while n / d == -1:
        n, d = sample(list(range(1, 9)) + list(range(-9, -2)), 2)
    a, b = sample(range(2, 9), 2)
    ee = (a * x + b) ** R(n, d)
    g = Struct(ee=sympy.sstr(ee))
    return g


def calc(g):
    res = sympy.sstr(S(sympy.integrate(S(g.ee), x)))
    return [res]
