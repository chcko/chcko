# -*- coding: utf-8 -*-

import random
import numpy as np
from chcko.hlp import Struct, norm_frac as norm


def given():
    k = np.array(random.sample(range(30, 60), 3))
    A = np.array([1, 0, 0] + random.sample(range(1, 19), 6))
    A.shape = (3, 3)
    Z = np.array(random.sample(range(1, 19), 3))
    m = np.array(random.sample(range(1, 19), 1))[0]
    g = Struct(k=k.tolist(), A=A.tolist(), Z=Z.tolist(), m=m)
    return g


def calc(g):
    axy = np.dot(g.A, g.k)
    z = np.dot(g.Z, axy)
    K = g.m * z
    return [K]
