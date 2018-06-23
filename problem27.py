#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 27:

Euler discovered the remarkable quadratic formula:

n^2+n+41
It turns out that the formula will produce 40 primes for the consecutive integer values 0≤n≤39. However, when n=40,
402+40+41=40(40+1)+41 is divisible by 41, and certainly when n=41,412+41+41 is clearly divisible by 41.

The incredible formula n^2−79n+1601 was discovered, which produces 80 primes for the consecutive values 0≤n≤79. The
product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:

n2+an+b, where |a|<1000 and |b|≤1000

where |n| is the modulus/absolute value of n
e.g. |11|=11 and |−4|=4
Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes
for consecutive values of n, starting with n=0.
"""

# Brute force, memoizing the prime-checking
# Not the most efficient, but completes in ~6 seconds

from math import sqrt
from itertools import count

memoized = {1: False}

def is_prime(n):
  if n < 0:
    return False
  if n in memoized:
    return memoized[n]
  
  prime = True
  
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      prime = False
      break
  
  memoized[n] = prime
  return prime

def num_primes_generated(coeffs):
  return next(i for i, n in enumerate(count(0)) if not is_prime(n**2 + coeffs[0]*n + coeffs[1]))

a, b = max(
  # If both are negative it'll produce a negative for n=0, which means 0 primes generated
  ((a, b) for a in range(-999, 1000) for b in range(-1000, 1001) if a > 0 or b > 0),
  key=num_primes_generated)
print(a*b)
