#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 124:

The radical of n, rad(n), is the product of the distinct prime factors of n. For example, 504 = 23 × 32 × 7, so rad(504)
= 2 × 3 × 7 = 42.

If we calculate rad(n) for 1 ≤ n ≤ 10, then sort them on rad(n), and sorting on n if the radical values are equal, we
get:

Unsorted       Sorted
n  rad(n)   n  rad(n)  k
1  1        1    1     1
2  2        2    2     2
3  3        4    2     3
4  2        8    2     4
5  5        3    3     6
6  6        9    3     6
7  7        5    5     7
8  2        6    6     8
9  3        7    7     9
10 10       10   10    10

Let E(k) be the kth element in the sorted n column; for example, E(4) = 8 and E(6) = 9.

If rad(n) is sorted for 1 ≤ n ≤ 100000, find E(10000).
"""

# The algorithm used is as follows:
# We start by generating all primes less than 100000 (the limit).
# We then use the algorithm described in problem88.py first to generate all combinations of prime factors such that the
# multiple is less than or equal to the limit, then to generate all numbers less than the limit with the same radical
# by incrementing the exponents on each combination of prime factors.
# Finally, we count numbers with the same radical, incrementing the radical until we have counted a total of just less
# than 10000 numbers, and adding the number of numbers with the next radical would put us over 10000 numbers counted.
# We sort that list and extract the 10000th number.
# This solution runs in about 1 second.

from itertools import compress, count

def product(s):
  r = 1
  for x in s:
    r *= x
  return r

LIMIT = 100001 # not 100000 because we need to include 100000 in the generated numbers
LOOKING_FOR = 10000

# Find primes less than limit using this apparently-fast prime sieve
sieve = bytearray([True]) * (LIMIT//2)

for i in range(3, int(LIMIT**0.5) + 1, 2):
  if sieve[i//2]:
    sieve[i*i//2::i] = bytearray((LIMIT-i*i-1)//(2*i)+1)

primes = [2, *compress(range(3, LIMIT, 2), sieve[1:])]

def gen_prime_combos(primes):
  # Generate all combinations of primes where the product is less than LIMIT
  for prime in primes:
    yield [prime]
  
  len_combo = 2
  while len_combo < len(primes) and product(primes[:len_combo]) < LIMIT:
    indexes = list(range(len_combo))
    last_incremented = 0
    
    while True:
      prod = product(primes[i] for i in indexes)
      while prod < LIMIT:
        yield [primes[i] for i in indexes]
        indexes[-1] += 1
        last_incremented = len_combo - 1
        prod = product(primes[i] for i in indexes)
      
      to_reset_to = last_incremented - 1
      if to_reset_to < 0:
        break
      
      indexes[to_reset_to] += 1
      for i in range(to_reset_to + 1, len_combo):
        indexes[i] = indexes[i - 1] + 1
      last_incremented = to_reset_to
    
    len_combo += 1

def gen_with_same_radical(p):
  # Given a list of primes factors p, generate all numbers with those same distinct prime factors less than LIMIT
  # (i.e. all combinations of exponents on the primes factors less than LIMIT)
  length = len(p)
  exponents = [1] * length
  last_incremented = length - 1
  
  while True:
    prod = product(p[i] ** exponents[i] for i in range(length))
    while prod < LIMIT:
      yield prod
      exponents[0] += 1
      last_incremented = 0
      prod = product(p[i] ** exponents[i] for i in range(length))
    
    to_increment = last_incremented + 1
    if to_increment >= length:
      break
    
    exponents[to_increment] += 1
    for i in range(to_increment):
      exponents[i] = 1
    last_incremented = to_increment

radical_lists = {1: [1]}

for i, p in enumerate(gen_prime_combos(primes)):
  radical_lists[product(p)] = list(gen_with_same_radical(p))

counted = 0
result = None

# Find the LOOKING_FORth number in radical_lists; sort only the list the LOOKING_FORth number is in
for radical in count(1):
  if radical in radical_lists:
    radical_list = radical_lists[radical]
    length = len(radical_list)
    
    if counted + length >= LOOKING_FOR:
      idx = LOOKING_FOR - counted - 1
      radical_list.sort()
      result = radical_list[idx]
      break
    else:
      counted += length

print(result)
