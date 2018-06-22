#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 10:

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""

# Sieve of Eratosthenes up to two million

up_to = 2000000

sieve = [True for _ in range(up_to)] # index + 1 is the number, value is whether it's prime or not
sieve[0] = False # 1 is not prime

# Do the sieve
for n in range(2, up_to + 1):
  for m in range(n * 2, up_to + 1, n):
    sieve[m - 1] = False

# Sum the True indices + 1
sum_ = sum(n + 1 for n in range(up_to) if sieve[n])
print(sum_)
