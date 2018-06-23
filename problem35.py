#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 35:

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves
prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""

# Sieve of Eratosthenes, then find circular primes

from math import sqrt

# Find the primes

sieve = [True for _ in range(1000000)] # index - 1 = number, value = prime
sieve[0] = False # 1 isn't prime

for n in range(2, len(sieve) // 2 + 1):
  if not sieve[n-1]:
    # only primes do sieving
    continue
  
  for m in range(2*n, len(sieve) + 1, n):
    sieve[m-1] = False

primes = {n + 1 for n, is_prime in enumerate(sieve) if is_prime}

# Find circular primes

def rotate(s, num):
  return s[num:] + s[:num]

num_circular = 0

for prime in list(primes):
  if prime not in primes:
    # it's been eliminated as an earlier prime's rotation
    continue
  
  all_rotations = {prime}
  prime_str = str(prime)
  
  for n in range(1, len(prime_str)):
    rotation = int(rotate(prime_str, n))
    
    if rotation in primes:
      all_rotations.add(rotation)
    else:
      break
  
  else:
    # all rotations were prime: it's circular
    num_circular += len(all_rotations)
    primes -= all_rotations

print(num_circular)
