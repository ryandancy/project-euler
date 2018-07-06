#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 52:

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different
order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""

from itertools import count

def digits(n):
  return set(str(n))

for x in count(1):
  if digits(2*x) == digits(3*x) == digits(4*x) == digits(5*x) == digits(6*x):
    print(x)
    break
