# -*- coding: utf-8 -*-
from random import randrange, sample
from chcko.hlp import Struct
import numpy as np


def given():
    n = 5
    x = sorted(sample(range(20), n))
    p = randrange(3, 6)
    ymax = p * x[n - 1]
    kf = randrange(1, ymax // 3)
    yf = lambda v: int((1.0 * (ymax - kf) / x[n - 1] / x[n - 1]) * v * v + kf)
    y = [yf(ax) for ax in x]
    g = Struct(x=x, y=y, p=p)
    return g


def calc(g):
    pf = np.polyfit(g.x, g.y, 2)
    pf = [-pf[0], g.p - pf[1], -pf[2]]
    xmax = np.roots(np.polyder(pf))
    ymax = np.polyval(pf, xmax)
    return [xmax[0], ymax[0]]
