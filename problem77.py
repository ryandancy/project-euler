#!/usr/bin/env python
# -*- coding: utf -*-

"""
Project Euler Problem 77:

It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?
"""

# The number of prime partitions can be calculated as so: k(n) = (sopf(n) + sum_{j=1}^{n-1} sopf(j)k(n - j))/n
# where sopf(n) = sum_{p in P, p|n} p (the sum-of-prime-factors function)
# (https://math.stackexchange.com/a/89661)
# Using sympy for the prime factors, runs in ~0.8 seconds

from sympy.ntheory import primefactors
from itertools import count

def sopf(n):
  return sum(primefactors(n))

memoized = {}
def count_prime_partitions(n):
  if n not in memoized:
    memoized[n] = (sopf(n) + sum(sopf(j) * count_prime_partitions(n - j) for j in range(1, n))) // n
  return memoized[n]

print(next(n for n in count(3) if count_prime_partitions(n) > 5000))
