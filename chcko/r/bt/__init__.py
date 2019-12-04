# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct

import sympy
from sympy import S, Rational as R
from sympy.abc import x


def given():
    a = 1
    b = R(randrange(3, 6))
    c = R('0.6') + randrange(5) * R(1, 10)
    e = c + randrange(4) * R(1, 10)
    d = a + randrange(5, 9)
    f = e + randrange(4, 7)
    j = f - R(1, 2)
    g = d + R(1, 2)
    h = d + randrange(4, 9)
    k = R(b - c, a * a)
    u = -k * x ** 2 + b
    v = (e - c) / (d - a) * (x - a) + c
    l = (f - e) / (h - d) ** R(1, 2)
    w = l * (x - d) ** R(1, 2) + e
    z = l * (x - d) ** R(1, 2)
    dc = Struct(
        u=sympy.sstr(u),
        v=sympy.sstr(v),
        w=sympy.sstr(w),
        z=sympy.sstr(z),
        d=d,
        g=g,
        h=h)
    return dc


def calc(dc):
    p1 = sympy.integrate(sympy.pi * S(dc.u) ** 2, (x, 0, 1))
    p2 = sympy.integrate(sympy.pi * S(dc.v) ** 2, (x, 1, S(dc.d)))
    p3 = sympy.integrate(sympy.pi * S(dc.w) ** 2, (x, S(dc.d), S(dc.h)))
    m4 = sympy.integrate(sympy.pi * S(dc.z) ** 2, (x, S(dc.g), S(dc.h)))
    res = S(p1 + p2 + p3 - m4).n()
    return [res]
