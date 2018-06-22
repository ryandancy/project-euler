#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 5:

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
"""

# Strategy: take the product of the common prime factors of 1 through 20

import math
from collections import Counter

def update_counter(counter, update):
  # "update" a counter by making sure that the count of each
  # key in the counter is greater than or equal to that in the update
  for key, count in update.items():
    if key not in counter or counter[key] < count:
      counter[key] = update[key]
  
  return counter


def get_prime_factors(n):
  # find the first factor
  try:
    factor1 = next(f for f in range(2, int(math.sqrt(n)) + 1) if n % f == 0)
  except StopIteration:
    # no factors: it's prime
    return (n,)
  
  factor2 = n // factor1
  
  return (*get_prime_factors(factor1), *get_prime_factors(factor2))


common_prime_factors = {}

# find the common prime factors
for n in range(1, 21):
  prime_factor_counts = Counter(get_prime_factors(n))
  common_prime_factors = update_counter(common_prime_factors, prime_factor_counts)

# multiply them all together to get the common LCM
product = 1
for factor, count in common_prime_factors.items():
  product *= factor ** count

print(product)
