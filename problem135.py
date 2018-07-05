#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 135:

Given the positive integers, x, y, and z, are consecutive terms of an arithmetic progression, the least value of the
positive integer, n, for which the equation, x^2 − y^2 − z^2 = n, has exactly two solutions is n = 27:

34^2 − 27^2 − 20^2 = 12^2 − 9^2 − 6^2 = 27

It turns out that n = 1155 is the least value which has exactly ten solutions.

How many values of n less than one million have exactly ten distinct solutions?
"""

# See problem136.py for an explanation
# Runs in ~2 minutes

from sympy.ntheory import divisors

num_ten_solutions = 0

for n in range(1, 1000000):
  num_solutions = 0
  n40 = 40*n
  n24 = 24*n
  for di in divisors(3072*n, generator=True):
    div_128 = di/128
    x = div_128 + n40/di
    
    if not x.is_integer():
      continue
    
    y = n24/di - div_128
    
    if y > 0 and y.is_integer():
      if num_solutions < 10:
        num_solutions += 1
      else:
        # multiple solutions
        break
  else:
    if num_solutions == 10:
      num_ten_solutions += 1

print(num_ten_solutions)
