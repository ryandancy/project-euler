#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 193:

A positive integer n is called squarefree, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are 
squarefree, but not 4, 8, 9, 12.

How many squarefree numbers are there below 2^50?
"""

# bleh, too slow

from itertools import compress

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

for i in range(1, len(squares)):
  print(total)
  for shift in range(len(squares) - i):
    adjust = LIMIT // product(squares[i:i+shift])
    total += -adjust if subtract else adjust
  subtract = not subtract

print(total)
