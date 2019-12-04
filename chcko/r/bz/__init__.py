# -*- coding: utf-8 -*-
from random import randrange
from math import pi, atan
from chcko.hlp import Struct


def given():
    g = Struct()
    g.l = randrange(21, 100)
    g.h = randrange(5, int(g.l / 2))
    return g


def calc(g):
    percentage = 100 * g.h / (g.l * g.l - g.h * g.h) ** 0.5
    angle = 180 * atan(g.h / (g.l * g.l - g.h * g.h) ** 0.5) / pi
    return [percentage, angle]
