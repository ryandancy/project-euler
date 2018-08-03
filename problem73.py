#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 73:

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d ≤ 12,000?
"""

# For each denominator between 4 and 12000 inclusive, we find the numerator that gives a fraction closest to 1/3 and 1/2
# Then we count coprimes between those two numerators inclusive
# Runs in ~5 seconds

from math import floor, ceil, gcd

num_fracs = 0

for denom in range(4, 12001):
  # find closest to 1/3, or greater
  numer_third = ceil(denom / 3)
  
  # find closest to 1/2, or smaller
  numer_half = floor(denom / 2)
  
  # count coprimes to denom between those two, inclusive
  for numer in range(numer_third, numer_half + 1):
    if gcd(numer, denom) == 1:
      num_fracs += 1

print(num_fracs)
