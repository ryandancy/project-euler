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
from math import factorial, sqrt

# from sympy.ntheory import mobius

def millis():
  return round(time() * 1000)

def product(x):
  r = 1
  for n in x:
    r *= n
  return r

prevtime = millis()

LIMIT = 1000 #2**50

# yields: [(product, start_next_at_idx), ...]
# def limited_products(pool, r, previous):
#   if r == 1:
#     yield [(p, i+1) for i, p in enumerate(pool)]
#   else:
#     # previous better not be None
#     for plist in previous:
#       for i, (p, start_next_at_idx) in enumerate(plist):
#         these_prods = []
#         for j, x in enumerate(pool[start_next_at_idx:]):
#           prod = x*p
#           if prod > LIMIT:
#             break
#           these_prods.append((prod, start_next_at_idx + j + 1))
#         if not these_prods:
#           break
#         yield these_prods
#       if i == 0:
#         break

# Use a sieve to generate primes below sqrt(2^50) = 2^25 and their squares
# This is apparently the fastest Python 3 prime sieve according to SO?

N = LIMIT#int(LIMIT**0.5)
sieve = bytearray([True]) * (N//2)

for i in range(3, int(N**0.5) + 1, 2):
  if sieve[i//2]:
    sieve[i*i//2::i] = bytearray((N-i*i-1)//(2*i)+1)

primes = [2, *compress(range(3, N, 2), sieve[1:])]
#squares = [x**2 for x in primes]

print('Found {} primes'.format(len(primes)))
#print(primes)

#### USE sum_{d=1}^{sqrt(LIMIT-1)} mu(d) * floor((n-1)/d^2)

# compact:
# print(sum(
#   mobius(d) * ((LIMIT - 1) // (d*d))
#   for d in range(1, int(sqrt(LIMIT - 1)))
# ))

# TOO MUCH MEMORY!!!!!
# Sieve?

# sum_ = 0
# MAX = int(sqrt(LIMIT - 1))
# for d in range(1, int(sqrt(LIMIT - 1))):
#   sum_ += mobius(d) * ((LIMIT - 1) // (d*d))
# print(sum_)

def binomial(n, k):
  try:
    return factorial(n) // factorial(k) // factorial(n - k)
  except ValueError:
    return 0

# YOU CAN GO BACKWARDS TOO KINDA SOMETIMES
def psi(diffs, offset=0, idx=0):
  if offset == len(diffs) - 2:
    return sum(diffs[0] + i for i in range(diffs[1] + idx))
  return sum(psi(diffs, offset + 1, i) for i in range(diffs[len(diffs)-offset-1] + idx))

def how_many_greater(found, len_primes):
  diffs = [*[found[i+1] - x for i, x in enumerate(found[:-1])], len_primes - found[-1] + 1]
  print(diffs)
  return psi(diffs)

# Number of squarefree is number of combinations of primes, b/c if prime factors have exponent >2 then not squarefree
total = len(primes) + 1 # to count 1 as squarefree

for num_primes in range(2, len(primes)):
  if product(primes[:num_primes]) > LIMIT:
    break
  
  # find lowest combo < limit
  found = []
  found_indices = []
  shift = 0
  for searching_primes in reversed(range(1, num_primes + 1)):
    while product(found + primes[shift:searching_primes+shift]) < LIMIT:
      shift += 1
      if shift > len(primes) - searching_primes:
        break
    else:
      found.append(primes[shift - 1])
      found_indices.append(shift)
  
  if not found:
    total += binomial(len(primes), num_primes)
    print('For {} primes, there are {} valid'.format(num_primes, binomial(len(primes), num_primes)))
    continue
  
  # find how many have primes greater than found, that's how many are bad
  greater = how_many_greater(found_indices, len(primes)) - 1
  total_number_primes = binomial(len(primes), num_primes)
  print(found, found_indices)
  print('For {} primes, there are {} greater (adding {})'.format(num_primes, greater, total_number_primes - greater))
  total += total_number_primes - greater

print(total)

# Use inclusion-exclusion to find the number of squarefree numbers

# total = LIMIT
# subtract = True
# lim_prods = None

# for i in count(1):
#   newtime = millis()
#   print('round ', i, ', total = ', total, ', time = ', newtime - prevtime, ' ms', sep='')
#   prevtime = newtime
  
#   lim_prods = list(limited_products(squares, i, lim_prods))
  
#   if not lim_prods:
#     break
  
#   #sys.stderr.write('-------------------------------------------\n')
  
#   for plist in lim_prods:
#     #sys.stderr.write(str(plist) + '\n')
#     for p, _ in plist:
#       #sys.stderr.write(str(p) + ', ' + str(_) + '\n')
#       adjust = LIMIT // p
#       total += -adjust if subtract else adjust
  
#   subtract = not subtract

# print(total)

from sympy.ntheory import primefactors

factors = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

def brute_force():
  total = 0
  for n in range(1, LIMIT):
    for prime in primes:
      if n % prime**2 == 0:
        break
    else:
      factors[len(primefactors(n))] += 1
      #sys.stderr.write(str(n) + ' | ' + str(factorint(n)) + '\n')
      #sys.stderr.write(str(n) + '\n')
      total += 1
  return total
print(brute_force())
print(factors)
