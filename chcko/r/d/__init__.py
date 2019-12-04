# -*- coding: utf-8 -*-
import numpy as np
import random
import itertools
from math import log
from sympy.abc import C, U, R, T
from sympy import E
from sympy import simplify

from chcko.hlp import Struct, norm_rounded

gc = np.array(range(500, 600, 10))  # μF
gu = np.array(range(900, 1000, 10))  # V
gr = np.array(range(150, 250, 10))  # kΩ
gt = np.array(range(20, 30))
curt = list(itertools.product(gc, gu, gr, gt))
num = len(gc) * len(gu) * len(gr) * len(gt)
ee = E ** (-T / (R * C))


def given():
    i = random.randrange(num)
    g = Struct()
    g.c, g.u, g.r, g.t = curt[i]
    g.u2 = g.u * E ** (-1e3 * g.t / (g.c * g.r))
    return g


def calc(g):
    # r,u,u2,t=230,940,773.54,26
    r, u, u2, t = g.r, g.u, g.u2, g.t
    c = 1e3 * t / (r * log(u / u2))
    return ['e^(-t/(R*C))',
            c,
            1e-6 * c * u,
            1e-6 * c * u2,
            1e-3 * r * c * log(2)]


def norm(answers):
    # answers=calc(given())
    try:
        e = simplify(answers[0].upper())
        a0 = str(e)
    except:
        a0 = answers[0]
    return [a0] + [norm_rounded(a, 2) for i, a in enumerate(answers) if i > 0]
