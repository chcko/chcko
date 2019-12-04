# -*- coding: utf-8 -*-

from random import randrange
from chcko.hlp import Struct, norm_rounded as norm

__all__ = ['given', 'norm', 'calc', 'g_fn', 'g_fs']

g_fn = [lambda a1, q, n:a1 + (n - 1) * q, lambda a1, q, n: a1 * q ** (n - 1)]
g_fs = [lambda a1,
        q,
        n:n * (2 * a1 + (n - 1) * q) / 2,
        lambda a1,
        q,
        n: a1 * (q ** n - 1) / (q - 1)]


def given():
    rr = randrange(2)  # 0 arithmetic, 1 geometric
    if rr == 0:
        a1 = randrange(-9, 9)
        q = randrange(1, 9)
    else:
        a1 = randrange(-9, 9)
        q = 1.0 + (1.0 * randrange(1, 9) / 100)
    g = Struct(rr=rr, a1=a1, q=q, n=randrange(4, 9), N=randrange(20, 60))
    return g


def calc(g):
    return [g_fn[g.rr](g.a1, g.q, g.n), g_fs[g.rr](g.a1, g.q, g.N)]
