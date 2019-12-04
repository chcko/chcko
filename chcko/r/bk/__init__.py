# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct, norm_int, norm_rounded
import numpy as np

__all__ = ['given', 'norm', 'calc', 'T']


def given():
    g = Struct()
    r2 = lambda v: round(
        randrange(int(v * 100 - v * 10), int(v * 100 + v * 10)) / 100.0, 2)
    r15 = lambda: randrange(1, 5)
    rr = lambda a, b: randrange(a, b)
    g.CC = [r15(), r15(), r15()]
    g.PP = [r2(1.8), r2(1), r2(0.3), r2(2.6)]
    g.RR = [[r2(80 / 250.0), r2(220 / 1000.0), rr(7, 10),
            r2(220 / 500.0)], [r2(150 / 250.0),
            r2(250 / 1000.0), rr(1, 3), r2(300 / 500.0)],
            [r2(70 / 250.0), r2(100 / 1000.0), rr(7, 9), 0]]
    return g

T = lambda x: np.transpose(np.array(x))


def calc(g):
    npR = T(g.RR)
    npM = np.array(g.PP)
    npC = np.array(g.CC)
    ingr = np.dot(npR, npC)
    money = np.dot(npM, ingr)
    return [int(ingr[2]), money]


def norm(answers):
    return [norm_int(answers[0]), norm_rounded(answers[1])]
