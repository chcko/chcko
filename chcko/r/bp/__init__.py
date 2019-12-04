# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct

import sympy
from sympy import S, Rational as R
from sympy.abc import x


def given():
    b = randrange(3, 6)
    c = b + randrange(4, 9)
    d = c + randrange(3, 6)
    u = randrange(1, 4)
    v = u + randrange(1, 4)
    w = v + randrange(1, 4)
    l = w / b ** R(1, 2)
    ff = l * x ** R(1, 2)
    gg = (u - w) * (x - b) / (c - b) + w
    hh = (v - u) * (x - c) / (d - c) + u
    t = randrange(3, 9)
    g = Struct(
        f=sympy.sstr(ff),
        g=sympy.sstr(gg),
        h=sympy.sstr(hh),
        b=b,
        c=c,
        d=d,
        t=t)
    return g


def calc(g):
    r1 = sympy.integrate(sympy.pi * S(g.f) ** 2, (x, 0, S(g.b)))
    r2 = sympy.integrate(sympy.pi * S(g.g) ** 2, (x, S(g.b), S(g.c)))
    r3 = sympy.integrate(sympy.pi * S(g.h) ** 2, (x, S(g.c), S(g.d)))
    vr = float(S(r1 + r2 + r3).n())
    s1 = sympy.integrate(2 * S(g.f), (x, 0, S(g.b)))
    s2 = sympy.integrate(2 * S(g.g), (x, S(g.b), S(g.c)))
    s3 = sympy.integrate(2 * S(g.h), (x, S(g.c), S(g.d)))
    vs = float(S((s1 + s2 + s3) * g.t).n())
    return [vs, vr]
