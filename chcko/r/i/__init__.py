# -*- coding: utf-8 -*-

import random
from sympy.abc import x
from sympy import log, latex
from chcko.hlp import Struct, norm_int as norm

jsFuncs = {'exp': 'return Math.pow(({0}),x-({1}))+({2})',
           'log': 'if (x-({0})>0) return Math.log(x-({0}))+({1})',
           'pow': 'return ({0})*Math.pow(x-({1}),({2}))+({3})'}


def given():
    # r,i,n,m=143,3,5,50
    N = 4
    rs = lambda r: random.sample(r, 1)[0]

    def gete():
        e = e0, e1, e2 = rs([0.2, 0.5, 2, 3]), rs(
            [-2, -1, 0, 1, 2]), rs([-2, -1, 0, 1, 2])
        ee = e0 ** (x - e1) + e2
        jse = jsFuncs['exp'].format(*e)
        return (latex(ee), jse)

    def getl():
        l = l0, l1 = rs([-2, -1, 0, 1, 2]), rs([-2, -1, 0, 1, 2])
        el = log(x - l0) + l1
        jsl = jsFuncs['log'].format(*l)
        return (latex(el), jsl)

    def getp():
        p = (p0, p1, p2, p3) = (
            rs([-2, -1, -1.0 / 2, 1.0 / 2, 1, 2]),
            rs([-2, -1, 0, 1, 2]),
            rs([-0.2, -0.5, -2, -3, 0.2, 0.5, 2, 3]),
            rs([-2, -1, 0, 1, 2]))
        ep = p0 * (x - p1) ** p2 + p3
        jsp = jsFuncs['pow'].format(*p)
        return (latex(ep), jsp)
    funcs = []
    while len(funcs) < N:
        f = rs([gete] * 100 + [getl] * 25 + [getp] * 1200)
        while True:
            nf = f()
            if nf not in funcs:
                funcs.append(nf)
                break
    order = range(len(funcs))
    random.shuffle(order)
    g = Struct(funcs=funcs, order=order)
    return g


def calc(g):
    return [o + 1 for o in g.order]
