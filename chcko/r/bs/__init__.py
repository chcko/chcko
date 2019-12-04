# -*- coding: utf-8 -*-
from random import sample
from chcko.hlp import Struct, equal_0 as equal, norm_expr as norm

import sympy
from sympy import S, sin, cos, E
from sympy.abc import x


def given():
    f = sample([E ** x, sin(x), cos(x), 1 / x], 1)[0]
    a, b = sample(range(2, 9), 2)
    ee = f.subs(x, a * x + b)
    g = Struct(ee=sympy.sstr(ee))
    return g


def calc(g):
    res = sympy.sstr(S(sympy.integrate(S(g.ee), x)))
    return [res]
