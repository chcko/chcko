# -*- coding: utf-8 -*-

import numpy as np
import random
from itertools import permutations
from chcko.hlp import Struct, norm_frac

pyt = [[3, 4], [5, 12], [6, 8], [4, 3], [12, 5],
       [8, 6], [-3, 4], [-5, 12], [-6, 8],
       [-4, 3], [-12, 5], [-8, 6], [3, -4],
       [5, -12], [6, -8], [4, -3], [12, -5], [8, -6]]
ipyt = 0
per = list(permutations([0, 1, 2]))


def given():
    global pyt, ipyt
    A = np.array(random.sample(range(-9, 10), 2))
    ipyt = (ipyt + 1) % len(pyt)
    d1 = np.array(pyt[ipyt])
    d2 = np.array([d1[1], -d1[0]])
    if random.random() > 0.5:
        d2 = -d2
    B = A + d1
    C = A + d2
    p = [A.tolist(), B.tolist(), C.tolist()]
    random.shuffle(p)
    g = Struct(p=p)
    return g


def calc(g):
    for i in per:
        a = np.array(g.p[i[1]]) - np.array(g.p[i[0]])
        b = np.array(g.p[i[2]]) - np.array(g.p[i[0]])
        if np.dot(a, b) == 0:
            break
    F = abs(np.linalg.det([a, b])) / 2
    return ["ABC"[i[0]], F]


def norm(answers):
    return [answers[0].upper(), norm_frac(answers[1])]
