#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 47:

The first two consecutive numbers to have two distinct prime factors are:

14 = 2 × 7
15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2^2 × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.

Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?
"""

# Generate prime factors, check for consecutives
# Runs in ~1.75 seconds

from math import sqrt
from collections import Counter
from itertools import count

memoized = {}
def prime_factors(n):
  if n not in memoized:
    for divisor in range(2, int(sqrt(n)) + 1):
      if n % divisor == 0:
        memoized[n] = prime_factors(divisor) + prime_factors(n // divisor)
        break
    else:
      memoized[n] = Counter({n: 1})
  
  return memoized[n]

def num_distinct_prime_factors(n):
  return len(prime_factors(n).keys())

print(next(n for n in count(1) if num_distinct_prime_factors(n) == 4
                              and num_distinct_prime_factors(n+1) == 4
                              and num_distinct_prime_factors(n+2) == 4
                              and num_distinct_prime_factors(n+3) == 4))
