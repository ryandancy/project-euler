#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 41:

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example,
2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""

# Generate pandigital numbers largest first, check if they're prime

from math import sqrt
from itertools import permutations

def is_prime(n):
  if n == 1:
    return False
  
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      return False
  
  return True

def largest_pandigital_prime():
  for num_digits in range(9, 0, -1):
    numbers = map(lambda digits: int(''.join(digits)), permutations(map(str, range(1, num_digits + 1)), num_digits))
    for n in sorted(numbers, reverse=True):
      if is_prime(n):
        return n
  return -1

print(largest_pandigital_prime())
