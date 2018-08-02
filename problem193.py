#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 193:

A positive integer n is called squarefree, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are 
squarefree, but not 4, 8, 9, 12.

How many squarefree numbers are there below 2^50?
"""

from time import time
from itertools import compress, combinations, count

def millis():
  return round(time() * 1000)

prevtime = millis()

def product(x):
  result = 1
  for n in x:
    result *= n
  return result

LIMIT = 2**50

def limited_products(pool, r, previous):
  if r == 1:
    yield from pool
  else:
    # previous better not be None
    for i, p in enumerate(previous):
      for x in pool[i+r-1:]:
        prod = x*p
        if prod > LIMIT:
          break
        yield prod
      else:
        continue
      if x == pool[i+r-1]:
        break
  
  # n = len(pool)
  # if r > n:
  #   return
  
  # indices = list(range(r))
  # yield product(pool[i] for i in indices)
  
  # revrange = list(reversed(range(r)))
  
  # while True:
  #   for i in revrange:
  #     if indices[i] != i + n - r:
  #       break
  #   else:
  #     return
    
  #   indices[i] += 1
  #   for j in range(i+1, r):
  #     indices[j] = indices[j-1] + 1
    
  #   p = product(pool[i] for i in indices)
  #   if p <= LIMIT:
  #     yield p
  #   elif i == 0:
  #     return
  #   else:
  #     indices[i-1] += 1
  #     for j in range(i, r):
  #       indices[j] = indices[j-1] + 1

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
lim_prods = None

for i in count(1):
  newtime = millis()
  print('round ', i, ', total = ', total, ', time = ', newtime - prevtime, ' ms', sep='')
  prevtime = newtime
  
  lim_prods = list(limited_products(squares, i, lim_prods))
  
  if not lim_prods:
    break
  
  for p in lim_prods:
    adjust = LIMIT // p
    total += -adjust if subtract else adjust
  
  subtract = not subtract

print(total)
