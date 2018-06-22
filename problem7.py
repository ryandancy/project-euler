#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 7:

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?
"""

# brute force

from math import sqrt

n = 1
num_primes = 0

while num_primes != 10001:
  n += 1
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      break
  else:
    # prime
    num_primes += 1

print(n)
