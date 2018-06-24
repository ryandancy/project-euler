#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left
to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37,
and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""

# Straightforward mostly brute-force
# Runs in ~6 seconds

from math import sqrt

memoized = {1: False}
def is_prime(n):
  if n in memoized:
    return memoized[n]
  
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      memoized[n] = False
      return False
  
  memoized[n] = True
  return True

def truncations_are_prime(digits, left=True):
  for i in range(1, len(digits)):
    truncation = int(digits[i:] if left else digits[:i])
    if not is_prime(truncation):
      return False
  return True

found = 0
sum_ = 0
n = 10

while found < 11:
  n += 1
  if not is_prime(n):
    continue
  
  digits = str(n)
  if not (truncations_are_prime(digits, left=True) and truncations_are_prime(digits, left=False)):
    continue
  
  found += 1
  sum_ += n

print(sum_)
