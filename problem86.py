#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 86:

A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a fly, F, sits in the opposite corner. By
travelling on the surfaces of the room the shortest "straight line" distance from S to F is 10.

However, there are up to three "shortest" path candidates for any given cuboid and the shortest route doesn't always
have integer length.

It can be shown that there are exactly 2060 distinct cuboids, ignoring rotations, with integer dimensions, up to a
maximum size of M by M by M, for which the shortest route has integer length when M = 100. This is the least value of M
for which the number of solutions first exceeds two thousand; the number of solutions when M = 99 is 1975.

Find the least value of M such that the number of solutions first exceeds one million.
"""

# Brute force, runs in ~1 hour

from math import sqrt

def is_integer_dimens(a, b, c):
  return sqrt(c**2 + (a + b)**2).is_integer()

def with_m(m):
  result = 0
  for b in range(1, m + 1):
    for c in range(1, b + 1):
      if is_integer_dimens(m, b, c):
        result += 1
  return result

sum_ = 0
m = 0
while sum_ < 10**6:
  if m % 100 == 0:
    print(m, sum_)
  m += 1
  sum_ += with_m(m)
print(m)
