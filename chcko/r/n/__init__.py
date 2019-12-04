# -*- coding: utf-8 -*-

import random
import numpy as np
from chcko.hlp import Struct


def given():
    a = random.sample(range(30, 50), 1)[0] * 1000
    b = random.sample(range(50, 100), 1)[0] * 1000
    n = random.sample(range(3, 6), 1)[0]
    k = random.sample(range(6, 12), 1)[0]
    y = np.array(range(1, n + 1))
    T = np.sum((y * a + b) / (1 + 1.0 * k / 100) ** y)
    c = round(T, -3)
    dd = (T - c)
    d = dd * random.sample(range(-4, 5), 1)[0]
    c = round(T + d, -3)
    g = Struct(a=a, b=b, c=c, n=n, k=k)
    return g


def calc(g):
    # g={'a':31000,'b':98000,'c':721000,'n':5,'k':9}
    y = np.array(range(1, g.n + 1))
    T = np.sum((y * g.a + g.b) / (1 + 1.0 * g.k / 100) ** y)
    dd = (T - g.c)
    return [T, 1 if dd > 0 else 2]
