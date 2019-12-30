# -*- coding: utf-8 -*-
import random
import math

from chcko.hlp import Struct

__all__ = ['given', 'calc', 'names']


def angle_deg(ai, g):
    '''
    >>> ai,g = 1,Struct(a=2,b=3,c=4)
    >>> int(angle_deg(1,g)+angle_deg(2,g)+angle_deg(3,g))
    180

    '''
    s = [g.a, g.b, g.c] * 2
    d = dict(zip('abc', (s[ai], s[ai + 1], s[ai + 2])))
    d['math'] = math
    return eval('180*math.acos((a*a+b*b-c*c)/2.0/a/b)/math.pi', d)


def given():
    random.seed()
    a, b = random.sample(range(1, 10), 2)
    c = random.randrange(max(a - b + 1, b - a + 1), a + b)
    return Struct(a=a, b=b, c=c)


def calc(g):
    return [angle_deg(i, g) for i in range(3)]


names = [r'\(\alpha=\)', r'\(\beta=\)', r'\(\gamma=\)']
