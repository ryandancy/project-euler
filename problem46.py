#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 46:

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a
square.

9 = 7 + 2×1^2
15 = 7 + 2×2^2
21 = 3 + 2×3^2
25 = 7 + 2×3^2
27 = 19 + 2×2^2
33 = 31 + 2×1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""

# Generate primes, squares, and odd composites, check each
# Probably not the most efficient (generating primes twice) but still runs in ~5 seconds

from itertools import count

def gen_primes():
  primes = set()
  for n in count(2):
    if not any(n % prime == 0 for prime in primes):
      yield n
      primes.add(n)

def gen_squares():
  for n in count(1):
    yield n**2

def is_prime_plus_twice_square(n):
  prime_gen = gen_primes()
  prime = next(prime_gen)
  
  while prime < n:
    square_gen = gen_squares()
    square = next(square_gen)
    
    while prime + 2*square < n:
      square = next(square_gen)
    
    if prime + 2*square == n:
      return True
    
    prime = next(prime_gen)
  
  return False

def gen_odd_composites():
  odd_primes = set()
  for n in count(3, step=2):
    if any(n % prime == 0 for prime in odd_primes):
      yield n
    else:
      odd_primes.add(n)

print(next(n for n in gen_odd_composites() if not is_prime_plus_twice_square(n)))
