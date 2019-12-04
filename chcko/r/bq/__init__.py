# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct

import random
import sympy
from sympy.abc import x


def given():
    g = Struct()
    g.w = randrange(400, 500)
    g.h = randrange(150, 250)
    g.dw = randrange(30, 40)
    g.dh = randrange(40, 50)
    g.d = randrange(300, 500)
    return g


def calc(g):
    w = g.w
    h = g.h
    dw = g.dw
    dh = g.dh
    d = g.d
    pi = x * (x - w)
    pimaxx = w / 2.0
    pimaxy = pi.subs(x, w / 2.0)
    pi = pi * h / abs(pimaxy)

    po = (x + dw) * (x - w - dw)
    pomaxx = w / 2.0
    pomaxy = po.subs(x, w / 2.0)
    po = po * (h + dh) / abs(pomaxy)

    ipo = sympy.integrate(-po, x)
    f1 = ipo.subs(x, 0) - ipo.subs(x, -dw)
    f2 = ipo.subs(x, w + dw) - ipo.subs(x, w)
    ipio = sympy.integrate(pi - po, x)
    f3 = ipio.subs(x, w) - ipio.subs(x, 0)
    f = f1 + f2 + f3
    v = f * d
    vm3 = v / 100.0 / 100.0 / 100.0

    return [vm3]
