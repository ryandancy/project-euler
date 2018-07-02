#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 49:

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i)
each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one
other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""

# Generate primes and permutations of each, check for arithmetic sequences
# Runs in ~100 ms

from itertools import permutations, combinations

def get_arithmetic_sequence_subset(nums):
  for combo in combinations(nums, 3):
    a, b, c = sorted(combo)
    if b - a == c - b > 0:
      return a, b, c
  return False

# Find all the 4-digit primes (and below) with the sieve of Erastothenes
is_prime = [True for _ in range(10000)] # index + 1 = num, value = is prime
is_prime[0] = False

for n in range(2, 10001):
  if not is_prime[n-1]:
    continue
  
  for i in range(2*n, 10001, n):
    is_prime[i-1] = False

# Generate permutations of each prime and check for arithmetic sequences
seen = set()

for prime in filter(lambda n: is_prime[n-1], range(1000, 10000)):
  if prime in seen:
    continue
  
  prime_permutations = list(
    filter(lambda n: is_prime[n-1],
           map(lambda x: int(''.join(x)),
               filter(lambda s: s[0] != '0', permutations(str(prime))))))
  
  if 1487 in prime_permutations:
    # don't generate the example
    continue
  
  sequence = get_arithmetic_sequence_subset(prime_permutations)
  if sequence:
    print(''.join(map(str, sequence)))
    break
  
  seen.update(prime_permutations)
