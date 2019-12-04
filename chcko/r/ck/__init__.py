# -*- coding: utf-8 -*-
from __future__ import division
from random import randrange
from chcko.hlp import Struct, norm_int as norm


def given():
    return Struct(
        A=randrange(150, 200), B=randrange(100, 150), C=randrange(50, 100)
    )


def calc(g):
    # g=given()
    # g=Struct(A=200,B=150,C=100)
    # total unknown but assumed known
    # p1=g.A/total
    # p2=g.B/total
    # p = p1*p2 #p1 and p2 independent
    # total*p = g.A*g.B/total = g.C
    total = g.A * g.B // g.C  # converts to int
    detected = g.A + g.B - g.C
    undetected = total - detected
    return [undetected]
