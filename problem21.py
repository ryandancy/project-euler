#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 21:

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable
numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The
proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""

import math

memoized_results = {1: 1}

def sum_of_proper_divisors(n):
  if n in memoized_results:
    return memoized_results[n]
  
  result = 1
  
  sqrt = math.sqrt(n)
  
  for divisor in range(2, int(sqrt)): # perfect squares will be dealt with later
    other_divisor, remainder = divmod(n, divisor)
    if remainder == 0:
      result += divisor
      result += other_divisor
  
  if sqrt.is_integer():
    # perfect square: the square root is also a proper divisor
    result += int(sqrt)
  
  memoized_results[n] = result
  return result

amicable_sum = 0

for a in range(2, 10000):
  b = sum_of_proper_divisors(a)
  if a != b and sum_of_proper_divisors(b) == a:
    amicable_sum += a

print(amicable_sum)
