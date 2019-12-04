# -*- coding: utf-8 -*-
import numpy as np
import random

from chcko.hlp import Struct


def given():
    A = np.array([1, 1] + random.sample(range(200, 1000), 2))
    A.shape = (2, 2)
    A = np.transpose(A)
    x = np.array(
        random.sample(
            range(
                500,
                1000),
            1) +
        random.sample(
            range(
                2,
                20),
            1))
    b = np.dot(A, x)
    g = Struct(A=A.tolist(), b=b.tolist())
    return g


def calc(g):
    iA = np.linalg.inv(np.array(g.A))
    x = np.dot(iA, np.array(g.b))
    return [i for i in x.round().tolist()]
