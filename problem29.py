#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 29:

Consider all integer combinations of a^b for 2 ≤ a ≤ 5 and 2 ≤ b ≤ 5:

2^2=4, 2^3=8, 2^4=16, 2^5=32
3^2=9, 3^3=27, 3^4=81, 3^5=243
4^2=16, 4^3=64, 4^4=256, 4^5=1024
5^2=25, 5^3=125, 5^4=625, 5^5=3125
If they are then placed in numerical order, with any repeats removed, we get the following sequence of 15 distinct
terms:

4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

How many distinct terms are in the sequence generated by a^b for 2 ≤ a ≤ 100 and 2 ≤ b ≤ 100?
"""

# We avoid evaluating massive powers by using the prime factors of each value of a
# We then multiply the numbers of prime factors by the exponent

# Prime factors are stored as a dictionary of {prime: exponent}
# Surprisingly, this is rather quick: runs in ~2.3 seconds

from math import sqrt

def add_dicts(d1, d2):
  result = d1.copy()
  for key in d2.keys():
    if key in result:
      result[key] += d2[key]
    else:
      result[key] = d2[key]
  return result

def multiply_dict(d, n):
  result = {}
  for key, value in d.items():
    result[key] = value * n
  return result

memoized = {}

def get_prime_factors(n):
  if n in memoized:
    return memoized[n]
  
  # Find first factor
  for factor1 in range(2, int(sqrt(n)) + 1):
    factor2, remainder = divmod(n, factor1)
    if remainder == 0:
      # found the first factor
      result = add_dicts(get_prime_factors(factor1), get_prime_factors(factor2))
      break
  else:
    # no factors: prime
    result = {n: 1}
  
  memoized[n] = result
  return result

distinct = []

for a in range(2, 101):
  prime_factors = get_prime_factors(a)
  
  for b in range(2, 101):
    exponent_prime_factors = multiply_dict(prime_factors, b)
    if exponent_prime_factors not in distinct:
      distinct.append(exponent_prime_factors)

print(len(distinct))
