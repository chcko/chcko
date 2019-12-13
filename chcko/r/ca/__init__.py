# -*- coding: utf-8 -*-

from chcko.hlp import Struct
import random
import numpy as np
from math import acos, pi

__all__ = ['given', 'calc']


def given():
    g = Struct()
    g.x = random.sample(range(-9, 9), 2)
    g.y = random.sample(range(-9, 9), 2)
    g.dx = random.sample(list(range(-4, -1)) + list(range(1, 4)), 1)[0]
    return g

angle = lambda a, b: 180 * \
    acos(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)) / pi
taria = lambda a, b: abs(np.cross(a, b) / 2)


def calc(g):
    a = angle(g.x, g.y)
    A = taria(g.x, g.y)
    nx = np.linalg.norm(g.x)
    ny = np.linalg.norm(g.y)
    x0 = g.x / np.linalg.norm(g.x)
    y0 = g.y / np.linalg.norm(g.y)
    A1 = taria(g.y, g.y + g.dx * x0)
    res = [a, A, nx, ny, x0[0], x0[1], y0[0], y0[1], A1]
    return res
