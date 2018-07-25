#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 60:

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order the
result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four primes,
792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.
"""

'''
This solution generates lists of valid concatenatable prime sets first of length 1 (i.e. every prime), then length 2, 3,
4, and finally 5, in order of their sums. It does this by, at each recursive step, looping through each prime up to the
lowest prime in the previous list and checking if it concatenates with each element in the previous list. The program
ends when the first length-5 prime set is generated. This program runs in approximately 12 minutes.
'''

from itertools import count
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

def gen_valid_prime_lists(howmany=5): # yields (list of primes, last_idx)
  if howmany == 1:
    yield from map(lambda n: ([nth_prime(n)], n), count())
  else:
    for valid, last_idx in gen_valid_prime_lists(howmany - 1):
      for prime_idx in range(last_idx):
        prime = primes[prime_idx] # it's less than the previous prime so primes will be filled in
        if is_pair_set(valid, prime):
          yield [*valid, prime], prime_idx

def is_pair_set(base_set, addition):
  for base in base_set:
    base_str = str(base)
    addition_str = str(addition)
    if not is_prime(int(base_str + addition_str)) or not is_prime(int(addition_str + base_str)):
      return False
  return True

if __name__ == '__main__':
  print(sum(next(gen_valid_prime_lists())[0]))
