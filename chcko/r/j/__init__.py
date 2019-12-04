# -*- coding: utf-8 -*-

import random
from sympy.abc import x
from sympy import exp, sin, cos, latex, Rational, S, N, integrate, sstr
from chcko.hlp import Struct

__all__ = ['given', 'calc', 'low', 'high']

rs = []
for i in [2, 3, 5]:
    for j in [2, 3, 5]:
        if i == j:
            continue
        rs.append(x ** Rational(i, j))
sp = [sin(x), cos(x), exp(x), 1 / x]

funs1 = rs[:]  # 1
for i in [2, 3, 5]:
    for j in [2, 3, 5]:
        if i == j:
            continue
        funs1 = funs1 + [Rational(i, j) * fun for fun in rs]

funs2 = sp[:]  # 1
for i in [2, 3, 5]:
    for j in [2, 3, 5]:
        if i == j:
            continue
        funs2 = funs2 + [Rational(i, j) * fun for fun in sp]

crange = range(3, 10)
low, high = 0.5, 1
""" #Any of funs1 - any of crange has no intersection with any of funs2 within low and high:
    #f2 > f1
from scipy.optimize import brentq
E=lambda f: lambda v: f.subs(x,v).evalf()
cnt = 0
for f1 in funs1:
    for f2 in funs2:
        for c in crange:
            try:
                res=N(integrate(f2-(f1-c),(x,low,high)))
                if res < 0.1:
                    print(res)
                brentq(E(f2-(f1-c)),low,high)
                cnt = cnt + 1 #found a root
            except ValueError:
                continue
print(cnt)#=> 0 => no root
"""


def given():
    ff1 = random.sample(funs1, 1)[0]
    f1 = ff1 - random.sample(crange, 1)[0]
    f2 = random.sample(funs2, 1)[0]
    g = Struct(f1=sstr(f1), f2=sstr(f2))
    return g


def calc(g):
    res = N(integrate(S(g.f2) - S(g.f1), (x, low, high)))
    return [res]
