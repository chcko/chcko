# -*- coding: utf-8 -*-
from random import randrange
from math import log
from chcko.hlp import Struct, norm_frac as norm


def given():
    g = Struct()
    g.C0 = randrange(20, 100) * 1000
    g.i = randrange(20, 40) / 10.0
    g.n = randrange(5, 10)
    g.r = randrange(300, 400)
    return g


def calc(g):
    q = (g.i / 100.0 + 1) ** (1.0 / 12)
    m = 12 * g.n
    Q = lambda n: q * (q ** n - 1) / (q - 1)
    monthlyrate = g.C0 * q ** m / Q(m)
    mm = -log(1 - g.C0 * (q - 1) / q / g.r) / log(q)
    fullmonths = int(mm)
    Cfullrate = g.r * Q(fullmonths)
    restrate = g.C0 * q ** fullmonths - Cfullrate
    restrate = q * restrate
    return [monthlyrate, fullmonths, restrate]
