# -*- coding: utf-8 -*-
from random import randrange, sample
from math import pi, sin
from chcko.hlp import Struct


def given():
    al, be = sample(range(10, 85), 2)
    c = randrange(2, 20)
    g = Struct(al=al, be=be, c=c)
    return g

##g = Struct(al=39,be=69,c=13)
#g = given()
# calc(g)


def calc(g):
    ga = 180 - g.be - g.al
    csga = g.c / sin(pi * ga / 180)
    a = sin(pi * g.al / 180) * csga
    b = sin(pi * g.be / 180) * csga
    return [a, b]
