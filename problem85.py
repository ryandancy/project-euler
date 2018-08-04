#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 85:

By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles. Although
there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with the
nearest solution.
"""

# The number of ways to select 2 gridlines (to form a rectangle) out of x gridlines is choose(x, 2)
# Thus on a X by Y grid, the number of rectangles is choose(x - 1, 2) * choose(y - 1, 2)
# choose(n, 2) = n!/(2!(n-2)!) = n!/(2(n-2)!)
# This solution will run forever until it is killed, but the correct solution is found within 0.1 seconds

from itertools import count
from math import factorial, ceil

def choose2(n):
  return factorial(n) // (2*factorial(n - 2))

closest_diff = 10**10
closest_area = 0

for x in count(2):
  for y in range(2, x):
    num_rects = choose2(x) * choose2(y)
    diff = abs(2000000 - num_rects)
    if diff < closest_diff:
      closest_diff = diff
      closest_area = (x - 1) * (y - 1)
      print('New closest: diff = {}, dimensions = {}x{}, area = {}'.format(closest_diff, x, y, closest_area))
