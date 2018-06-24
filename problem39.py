#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 39:

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions
for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000 is the number of solutions maximised?
"""

# Generate all Pythagorean triplets that add to <= 1000 and count sums

from collections import defaultdict
from math import sqrt

pythag_sums = defaultdict(lambda: 0)

a = 0
while a <= 1000:
  b = c = 0
  
  while a + b + c <= 1000:
    b += 1
    c = sqrt(a**2 + b**2)
    if c.is_integer():
      pythag_sums[a + b + int(c)] += 1
    
  a += 1

print(max(pythag_sums.keys(), key=lambda val: pythag_sums[val]))
