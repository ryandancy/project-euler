#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 127:

The radical of n, rad(n), is the product of distinct prime factors of n. For example, 504 = 23 × 32 × 7, so rad(504) =
2 × 3 × 7 = 42.

We shall define the triplet of positive integers (a, b, c) to be an abc-hit if:

1. GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
2. a < b
3. a + b = c
4. rad(abc) < c

For example, (5, 27, 32) is an abc-hit, because:

1. GCD(5, 27) = GCD(5, 32) = GCD(27, 32) = 1
2. 5 < 27
3. 5 + 27 = 32
4. rad(4320) = 30 < 32

It turns out that abc-hits are quite rare and there are only thirty-one abc-hits for c < 1000, with ∑c = 12523.

Find ∑c for c < 120000.
"""

# Not a terribly efficient algorithm, but some optimizations have been used
# Prime factorization is delegated to sympy because it's slightly faster than doing it ourselves
# Runs in ~1 hour 20 minutes (optimized down from 3 hours)

from math import sqrt, ceil, gcd
from sympy.ntheory import primefactors
import sys

memoized = {}
def distinct_prime_factors(n):
  if n in memoized:
    return memoized[n]
  result = primefactors(n)
  memoized[n] = result
  return result

def rad_abc_less_than_c(a, b, c):
  # testing c, b, a because that's in order of size
  product = 1
  
  for m in distinct_prime_factors(c):
    product *= m
  
  # Prime factors of c will only ever possibly multiply to equal c
  if product == c:
    return False
  
  for m in distinct_prime_factors(b):
    product *= m
    if product >= c:
      return False
  
  for m in distinct_prime_factors(a):
    product *= m
    if product >= c:
      return False
  
  return True

sum_c = 0
found = 0

for c in range(2, 120000):
  if c % 100 == 0:
    sys.stdout.write('\rFound: {} | Sum: {} | Testing: {}'.format(found, sum_c, c))
    sys.stdout.flush()
  
  for a in range(1, ceil(c/2)):
    if gcd(a, c) != 1:
      continue
    
    b = c - a
    
    if gcd(a, b) != 1 or gcd(b, c) != 1:
      continue
    
    if rad_abc_less_than_c(a, b, c):
      sum_c += c
      found += 1

print('\n')
print(sum_c)
