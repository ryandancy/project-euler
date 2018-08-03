#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 72:

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions for d ≤ 1,000,000?
"""

# The number of coprimes to n less than n is phi(n) where phi(n) is Euler's totient function
# Therefore this problem asks for sum_{i=2}^1000000 phi(i)
# sum_{i=1}^n phi(i) = (1 + sum_{i=1}^n mu(n)*floor(n/i)^2) / 2, then subtract 1 to remove 1/1 as a possibility
# (sum_{i=1}^{10^6} phi(i) was computed at https://oeis.org/A064018, but this works too)
# Runs in ~3 minutes and consumes ~1 GB of RAM

from sympy.ntheory import mobius

n = 1000000

print((sum(
  mobius(i) * (n // i)**2
  for i in range(1, n + 1)
) + 1) // 2 - 1)
