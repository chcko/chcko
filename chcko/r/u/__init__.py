# -*- coding: utf-8 -*-

import numpy as np
import random

from chcko.hlp import Struct, norm_frac as norm


def given():
    while True:
        A = np.array(random.sample(range(-5, 6), 4))
        A.shape = (2, 2)
        try:
            m = np.linalg.inv(A)
            A = np.linalg.inv(np.array(m))
        except:
            continue
        break
    g = Struct(m=m.tolist())
    return g


def calc(g):
    A = np.linalg.inv(np.array(g.m))
    A = A.round()
    r = [A[0, 0], A[0, 1], A[1, 0], A[1, 1]]
    return [i for i in r]
