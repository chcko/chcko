# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct
from datetime import datetime, timedelta


def given():
    g = Struct()
    g.K0 = randrange(20, 100) * 1000
    g.d1 = datetime.now() - timedelta(days=randrange(300)) - \
        timedelta(days=365)
    g.d2 = datetime.now() + timedelta(days=randrange(300)) + \
        timedelta(days=365)
    g.i = 1.0 + 1.0 * randrange(20) / 10
    return g


def calc(g):
    K0 = g.K0
    i = g.i
    d1 = g.d1
    d2 = g.d2
    d1d = 30 * (12 - d1.month) + ((30 - d1.day) if d1.day <= 30 else 0)
    d2d = 30 * (d2.month - 1) + d2.day
    n = d2.year - d1.year - 1
    q1 = 1 + i * d1d / 360.0 / 100
    q2 = 1 + i * d2d / 360.0 / 100
    q = 1 + i / 100.0
    Kn1 = K0 * q1 * q ** n * q2
    nf = n + d1d / 360.0 + d2d / 360.0
    Kn2 = K0 * q ** nf
    dKn = Kn1 - Kn2
    return [Kn1, dKn]
