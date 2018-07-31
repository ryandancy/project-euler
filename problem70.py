#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 70:

Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine the number of positive numbers
less than or equal to n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine
and relatively prime to nine, φ(9)=6.

The number 1 is considered to be relatively prime to every positive number, so φ(1)=1.

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and the ratio n/φ(n) produces a minimum.
"""

# Fairly brute-force, takes ~15 minutes to run

from sympy.ntheory import primefactors
from functools import reduce
import operator

def phi(n):
  return round(n * reduce(operator.mul, map(lambda p: 1 - 1/p, primefactors(n))))

def is_permutation(n, m):
  return sorted(str(n)) == sorted(str(m))

min_ratio = 10**10
min_n = 0

for n in range(2, 10**7 + 1):
  if n % 10000 == 0:
    print(n)
  
  p = phi(n)
  ratio = n/p
  if ratio < min_ratio and is_permutation(n, p):
    min_ratio = ratio
    min_n = n

print(min_n)
