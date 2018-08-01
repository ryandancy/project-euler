#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 193:

A positive integer n is called squarefree, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are 
squarefree, but not 4, 8, 9, 12.

How many squarefree numbers are there below 2^50?
"""

from time import time
from itertools import compress, combinations

def millis():
  return round(time() * 1000)

prevtime = millis()

def product(x):
  result = 1
  for n in x:
    result *= n
  return result

LIMIT = 2**50

# Use a sieve to generate primes below sqrt(2^50) = 2^25 and their squares
# This is apparently the fastest Python 3 prime sieve according to SO?

N = int(LIMIT**0.5)
sieve = bytearray([True]) * (N//2)

for i in range(3, int(N**0.5) + 1, 2):
  if sieve[i//2]:
    sieve[i*i//2::i] = bytearray((N-i*i-1)//(2*i)+1)

squares = [4, *map(lambda x: x*x, compress(range(3, N, 2), sieve[1:]))]

print('Found {} squares'.format(len(squares)))

# Use inclusion-exclusion to find the number of squarefree numbers

total = LIMIT
subtract = True

# works, but still too slow

for i in range(1, len(squares) + 1):
  newtime = millis()
  print(i, '/', len(squares), ' iterations, total = ', total, ', time = ', newtime - prevtime, ' ms', sep='')
  prevtime = newtime
  # for shift in range(len(squares) - i + 1):
    # adjust = LIMIT // product(squares[shift:i+shift])
  
  for combo in combinations(squares, i):
    if combo[0]**i > LIMIT:
      break
    p = product(combo)
    if p > LIMIT:
      continue
    adjust = LIMIT // p
    total += -adjust if subtract else adjust
  
  # products = list(map(product, zip(products, squares[i:])))
  # products = [
  #   p1*p2
  #   for i, p1 in enumerate(products)
  #   for p2 in squares[i:]
  #   if p1*p2 <= LIMIT
  # ]
  subtract = not subtract

print(total)
