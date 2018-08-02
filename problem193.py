#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 193:

A positive integer n is called squarefree, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are 
squarefree, but not 4, 8, 9, 12.

How many squarefree numbers are there below 2^50?
"""

import sys
from time import time
from itertools import compress, count

def millis():
  return round(time() * 1000)

prevtime = millis()

LIMIT = 6000000#2**50

# yields: [(product, start_next_at_idx), ...]
def limited_products(pool, r, previous):
  if r == 1:
    yield [(p, i+1) for i, p in enumerate(pool)]
  else:
    # previous better not be None
    for plist in previous:
      for i, (p, start_next_at_idx) in enumerate(plist):
        these_prods = []
        for j, x in enumerate(pool[start_next_at_idx:]):
          prod = x*p
          if prod > LIMIT:
            break
          these_prods.append((prod, start_next_at_idx + j + 1))
        if not these_prods:
          break
        yield these_prods
      if i == 0:
        break

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
  
  sys.stderr.write('-------------------------------------------\n')
  
  for plist in lim_prods:
    sys.stderr.write(str(plist) + '\n')
    for p, _ in plist:
      #sys.stderr.write(str(p) + ', ' + str(_) + '\n')
      adjust = LIMIT // p
      total += -adjust if subtract else adjust
  
  subtract = not subtract

print(total)

def brute_force():
  total = 0
  for n in range(1, LIMIT + 1):
    for square in squares:
      if n % square == 0:
        break
    else:
      total += 1
  return total
print(brute_force())
