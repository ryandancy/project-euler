#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 50:

The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""

# Generate primes with the sieve of Erastosthenes, generate consecutive sums most to least, check if each is prime
# Runs in ~4 minutes

is_prime = [True for _ in range(1000000)] # index + 1 = num, value = is prime
is_prime[0] = False

primes = []

for n in range(1, 1000001):
  if not is_prime[n-1]:
    continue
  
  for i in range(2*n, 1000001, n):
    is_prime[i-1] = False
  
  # We know there's at least 21 (example with 1000) so we can drastically reduce the search space
  # Primes over 50000 times 20 are greater than 1000000, so we can eliminate them
  if n < 50000:
    primes.append(n)

memoizedr = {}
def memoized_sum_recursive(start, end):
  if (start, end) not in memoizedr:
    if start == end - 1:
      memoizedr[(start, end)] = primes[start]
    else:
      memoizedr[(start, end)] = memoized_sum_recursive(start, end - 1) + primes[end - 1]
  return memoizedr[(start, end)]

memoized = {}
def memoized_sum(start, end):
  result = 0
  s, e = start, end
  while True:
    if (s, e) in memoized:
      result += memoized[(s, e)]
      break
    elif s == e - 1:
      memoized[(s, e)] = primes[s]
      result += primes[s]
      break
    else:
      result += primes[e - 1]
      e -= 1
  memoized[(start, end)] = result
  return result

def gen_consecutive_prime_sums():
  for num_primes in range(len(primes), 0, -1):
    for start in range(len(primes) - num_primes + 1):
      yield sum(primes[start : start + num_primes])

print(next(n for n in gen_consecutive_prime_sums() if n < 1000000 and is_prime[n-1]))
