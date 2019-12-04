# -*- coding: utf-8 -*-
import numpy as np
import random

from chcko.hlp import Struct


def given():
    cf = random.sample(range(2000, 2500), 1)[0]
    m1 = random.sample(range(30, 45), 1)[0]
    m2 = random.sample(range(50, 70), 1)[0]
    A = np.array([[m1 * m1, m1], [m2 * m2, m2]])
    x1 = random.sample(range(-5, -1), 1)[0]
    x2 = random.sample(range(300, 999), 1)[0]
    x = np.array([x1, x2])
    b = np.dot(A, x)
    c1 = b[0] + cf
    c2 = b[1] + cf
    g = Struct(A=A.tolist(), b=b.tolist(), cf=cf)
    return g


def calc(g):
    iA = np.linalg.inv(np.array(g.A))
    x = np.dot(iA, np.array(g.b))
    x = x.tolist()
    return [i for i in (x + [g.cf])]
