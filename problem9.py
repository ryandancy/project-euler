#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 9:

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""

# Loop through a and b such that a < b, calculating c, and checking if a + b + c = 1000

from math import sqrt

def find_triplet_with_sum(n):
  b = 1
  while True:
    b += 1
    for a in range(1, b):
      c = sqrt(a**2 + b**2)
      if a + b + c == n:
        # c has to be an integer because otherwise it wouldn't sum with two integers to an integer
        return a, b, int(c)

a, b, c = find_triplet_with_sum(1000)
print(a*b*c)
