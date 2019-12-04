# -*- coding: utf-8 -*-
from random import randrange, sample
from chcko.hlp import Struct


def given():
    i1 = randrange(15, 90) / 10.0
    di = (randrange(1, 10) - 5) / 50.0
    if di == 0:
        di = 0.05
    i2 = i1 + di
    i_c = [4, 12, 1]
    i = [ii for ii in sample(i_c, 2)]
    i_n = ['i_' + str(ii) for ii in i]
    clc = lambda ai, ii: '{:.2f}'.format(
        100 * ((ai / 100.0 + 1.0) ** (1.0 / ii) - 1))
    i_v = [clc(i1, i[0]), clc(i2, i[1])]
    g = Struct(
        i1=i[0],
        i2=i[1],
        i1n=i_n[0],
        i2n=i_n[1],
        i1v=i_v[0],
        i2v=i_v[1])
    return g


def calc(g):
    res = 2 if (
        (1 +
         float(
             g.i1v) /
            100.0) ** g.i1 -
        1 < (
            1 +
            float(
                g.i2v) /
            100.0) ** g.i2 -
        1) else 1
    return [res]
