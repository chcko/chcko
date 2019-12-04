# -*- coding: utf-8 -*-
import random
from sympy import Poly, solve
from sympy.abc import x

from chcko.hlp import Struct, norm_int, norm_frac


def given():
    p = 0
    x1 = x2 = 0
    while p == 0 and x1 == x2:  # p could become 0
        x1, x2 = random.sample(range(2, 9) + range(-9, -2), 2)
        p = -(x1 + x2)
        q = x1 * x2
    a = random.sample(range(2, 6) + range(-5, -1), 1)[0]
    b = p * a
    c = q * a
    g = Struct(coef=[a, b, c])
    return g


def calc(g):
    # g=given()
    p = Poly(g['coef'], x, domain='ZZ')
    x1, x2 = solve(p)
    xs = 1.0 * (x1 + x2) / 2
    ys = p(xs)
    answers = [
        norm_int(x1) +
        ', ' +
        norm_int(x2),
        norm_frac(xs) +
        ',' +
        norm_frac(ys)]
    return answers


def norm(answers):
    #answers = calc(given())
    a = answers[:]
    res = a[0]
    try:
        sa = sorted([norm_int(aa) for aa in a[0].split(',')])
        if len(sa) == 1:
            res = sa * 2
        else:
            res = sa
    except:
        pass
    a[0] = ','.join(res)
    a[1] = ','.join([norm_frac(aa) for aa in a[1].split(',')])
    return a
