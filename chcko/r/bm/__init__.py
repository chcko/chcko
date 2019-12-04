# -*- coding: utf-8 -*-
from random import randrange
from chcko.hlp import Struct, norm_expr, norm_rounded, equal_0 as equal
import sympy
from sympy import S, Rational as R, latex
from sympy.abc import x


def given():
    xp0 = randrange(7, 10)
    pmax = randrange(7, 10)
    Ep = R(-pmax, xp0) * x + pmax
    E = sympy.integrate(Ep, x)
    b = randrange(2, xp0 - 2)
    cmax = int(Ep.subs(x, b).n())
    c = randrange(1, cmax)
    a = R(randrange(1, pmax - c), b * b)
    Kp = a * (x - b) ** 2 + c
    Gp = Ep - Kp
    rG = [r.n() for r in sympy.roots(Gp) if r > 0][0]
    G = sympy.integrate(Gp, x)
    mG = G.subs(x, rG)
    Ko = int(mG - 1) / 2
    #K = sympy.integrate(Kp,x)+Ko
    #G = E.n()-K.n()
    #rts = sorted([r.n() for r in sympy.roots(G) if r > 0])
    g = Struct(pmax=pmax, xp0=xp0, Ko=Ko, Kp=sympy.sstr(Kp))
    return g


def norm(a):
    res = [norm_expr(aa) for aa in a[:5]] + norm_rounded(a[5:], 2)
    return res


def calc(g):
    Kp = S(g.Kp)
    Ep = R(-g.pmax, g.xp0) * x + g.pmax
    E = sympy.integrate(Ep, x)
    K = sympy.integrate(Kp, x) + S(g.Ko)
    Gp = Ep - Kp
    rG = [r.n() for r in sympy.roots(Gp) if r > 0][0]
    G = E - K
    mG = G.subs(x, rG)
    kk = sympy.Wild('kk')
    dd = sympy.Wild('dd')
    kd = Ep.match(kk * x + dd)
    p = kd[kk] * x / 2 + kd[dd]
    mp = p.subs(x, rG)
    el = S(1 + kd[dd] / (kd[kk] * x / 2))
    return [
        sympy.sstr(Ep),
        sympy.sstr(E),
        sympy.sstr(K),
        sympy.sstr(p),
        sympy.sstr(el),
        rG,
        mp]
