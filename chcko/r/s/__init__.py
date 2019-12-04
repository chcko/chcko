# -*- coding: utf-8 -*-

import numpy as np
import random

from chcko.hlp import Struct


def given():
    p1, p2 = random.sample(range(20, 30), 2)
    p0 = random.sample(range(140, 150), 1)[0]
    pp0 = random.sample(range(51, 60), 1)[0]
    A = np.array([np.array([p0, p1, p2]) / 10.0,
                  np.array([-pp0 / 100.0, 1, 1]),
                  np.array([1, 1, 1])])
    x0 = 100. / (100. + pp0)
    pp12 = pp0 / (100. + pp0)
    x1 = random.sample(range(1, int(100. * pp12)), 1)[0] / 100.0
    x2 = pp12 - x1
    x = np.array([x0, x1, x2])
    b = np.dot(A, x)
    g = Struct(A=A.tolist(), b=b.tolist())
    return g


def calc(g):
    iA = np.linalg.inv(np.array(g.A))
    x = np.dot(iA, np.array(g.b))
    return [i for i in (100 * x).round().tolist()]
