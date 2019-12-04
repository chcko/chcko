# -*- coding: utf-8 -*-
import random
from math import log
from chcko.hlp import Struct


def given():
    g = Struct()
    g.pc = random.randrange(10, 90)
    return g


def calc(g):
    t = -log(g.pc / 100.0) * 5730 / log(2)
    return [t]

#import sympy
#from sympy.abc import x
#th = 5730
# lambda = sympy.ln(2)/th
# lambda.n()
# c14 = sympy.exp(-lambda*x)
#nc14 = lambda v:sympy.N(c14.subs(x,v))
# nc14(5730)
#t = -log(g['pc']/100.0)*5730/log(2)
#
