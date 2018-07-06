#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 141:

A positive integer, n, is divided by d and the quotient and remainder are q and r respectively. In addition d, q, and r
are consecutive positive integer terms in a geometric sequence, but not necessarily in that order.

For example, 58 divided by 6 has quotient 9 and remainder 4. It can also be seen that 4, 6, 9 are consecutive terms in a
geometric sequence (common ratio 3/2). We will call such numbers, n, progressive.

Some progressive numbers, such as 9 and 10404 = 102^2, happen to also be perfect squares.
The sum of all progressive perfect squares below one hundred thousand is 124657.

Find the sum of all progressive perfect squares below one trillion (10^12).
"""

# A far less efficient algorithm, runs in O(2^n) instead of O(n^2)

def is_perfect_cube(n):
  return int(round(n**(1/3)))**3 == n

sum_ = 0

for k in range(1, 1000000):
  n = k**2
  k4 = k**4
  for x in (k4 - i**2 for i in range(k % 2, n, 2)):
    d3 = x/4
    d = int(round(d3**(1/3)))
    if d**3 == d3 and d < k:
      sum_ += n
      print('Found: d={}, n={}'.format(round(d3**(1/3)), n))
      break

print(sum_)
