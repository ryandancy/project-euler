#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 3:

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""

import math

num = 600851475143

def get_prime_factors(n):
  factors = set()
  
  for fac1 in range(2, int(math.sqrt(n))):
    fac2, remainder = divmod(n, fac1)
    if remainder != 0:
      # not a factor
      continue
    factors.update(get_prime_factors(fac1))
    factors.update(get_prime_factors(fac2))
  
  return factors or {n}

print(max(get_prime_factors(num)))
