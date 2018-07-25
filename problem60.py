#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 60:

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order the
result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four primes,
792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.
"""

from itertools import count, permutations
from math import sqrt

primes = []
def gen_primes():
  for n in count(2):
    for prime in primes:
      if n % prime == 0:
        break
    else:
      primes.append(n)
      yield

prime_gen = gen_primes()
def nth_prime(n):
  while n >= len(primes):
    next(prime_gen)
  return primes[n]

def is_prime(n):
  # faster than a gen_primes()-based method, apparently "primes[-1]" is expensive
  if n in primes:
    return True
  
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      return False
  
  return True

invalid_subsets = []

def gen_prime_sets(howmany=5, max_=None, add=set()):
  if howmany == 0:
    yield add
    return
  
  # exclude the 0th prime (2) because it can't be in a prime pair set
  for n in count(howmany) if max_ is None else range(howmany, max_):
    if howmany == 5: print(n)
    
    add2 = add | {nth_prime(n)}
    
    for invalid in invalid_subsets:
      if invalid < add2:
        break
    else:
      yield from gen_prime_sets(howmany - 1, n, add2)

def is_pair_set(prime_set):
  for pair in permutations(prime_set, 2):
    pair_num = int(''.join(map(str, pair)))
    if not is_prime(pair_num):
      invalid_subsets.append(set(pair))
      return False
  return True

if __name__ == '__main__':
  print(sum(next(prime_set for prime_set in gen_prime_sets() if is_pair_set(prime_set))))
