#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 76:

It is possible to write five as a sum in exactly six different ways:

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?
"""

# Using a (naive) implementation of the Hardy-Ramanujan-Rademacher formula, this runs in less than 0.1 seconds.
# This implementation of the HRR formula isn't particularly inaccurate for p(10000) (as verified by Wolfram Alpha),
# but seems to do fine for p(100).

from math import pi, cos, sinh, cosh, sqrt, ceil

def U(x):
  return cosh(x) - (sinh(x) / x)

def C(n):
  return pi/6 * sqrt(24*n - 1)

def A(k, n):
  return sqrt(k/3) * sum(
    (-1)**l * cos(pi * (6*l + 1)/(6*k))
    for l in range(2*k)
    if ((3*l*l + l) / 2) % k == -n % k
  )

def p(n):
  N = ceil(sqrt(n)) * 2
  return round(sum(
    sqrt(3/k) * (4/(24*n - 1)) * A(k, n) * U(C(n)/k)
    for k in range(1, N + 1)
  ))

print(p(100) - 1)
