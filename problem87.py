#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 87:

The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28. In fact, there
are exactly four numbers below fifty that can be expressed in such a way:

28 = 2^2 + 2^3 + 2^4
33 = 3^2 + 2^3 + 2^4
49 = 5^2 + 2^3 + 2^4
47 = 2^2 + 3^3 + 2^4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?
"""

# Brute force but with optimizations
# We first generate all primes < sqrt(LIMIT), then iterate through ways to combine squares, cubes, and hypercubes
# Some are the same, so we add them to a set and take the length of the set at the end
# (this is why finding the highest prime that hypercubed gives < LIMIT for any given square/cube pair won't work)
# If the sum at any point is too high, we break out of that loop
# Runs in ~2 seconds

from itertools import compress

LIMIT = 50000000

# find primes using this super weird but fast sieve from SO
N = int(LIMIT**0.5)
sieve = bytearray([True]) * (N//2)

for i in range(3, int(N**0.5) + 1, 2):
  if sieve[i//2]:
    sieve[i*i//2::i] = bytearray((N-i*i-1)//(2*i)+1)

primes = [2, *compress(range(3, N, 2), sieve[1:])]

expressable = set()
for a in primes:
  a2 = a**2
  if a2 >= LIMIT:
    break
  for b in primes:
    a2b3 = a2 + b**3
    if a2b3 >= LIMIT:
      break
    for c in primes:
      expressed = a2b3 + c**4
      if expressed >= LIMIT:
        break
      expressable.add(expressed)
print(len(expressable))
