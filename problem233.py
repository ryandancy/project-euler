#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 233:

Let f(N) be the number of points with integer coordinates that are on a circle passing through (0,0), (N,0),(0,N), and
(N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420 ?
"""

import sys
from itertools import count
from sympy.ntheory import factorint

def f(n):
  r = 1
  for p, e in factorint(n).items():
    if p % 4 == 1:
      r *= 2*e + 1
  return 4*r

primes = set()
def gen_primes():
  for n in count(2):
    for prime in primes:
      if n % prime == 0:
        break
    else:
      primes.add(n)
      yield n

primes_1mod4 = []
primes_non_1mod4 = []
primes_generator = gen_primes()

def sort_next_prime():
  next_prime = next(primes_generator)
  if next_prime % 4 == 1:
    primes_1mod4.append(next_prime)
  else:
    primes_non_1mod4.append(next_prime)

def nth_prime_1mod4(n): # zero-indexed
  while n >= len(primes_1mod4):
    sort_next_prime()
  return primes_1mod4[n]

def nth_prime_non_1mod4(n): # also zero-indexed
  while n >= len(primes_non_1mod4):
    sort_next_prime()
  return primes_non_1mod4[n]

LIMIT = 10**11

def total_for_1mod4_combo(base_num, highest_non_1mod4_idx=None):
  this_total = 0
  
  if highest_non_1mod4_idx is None:
    highest_non_1mod4_idx = 0
    
    while base_num * nth_prime_non_1mod4(highest_non_1mod4_idx) <= LIMIT:
      this_total += total_for_1mod4_combo(base_num, highest_non_1mod4_idx)
      highest_non_1mod4_idx += 1
      #print(base_num, this_total, highest_non_1mod4_idx)
    
    return this_total + 1 # adding 1 for the all 0s case
  elif highest_non_1mod4_idx == -1:
    sys.stderr.write(str(base_num) + '\n')
    return 1
  
  highest_non_1mod4_prime = nth_prime_non_1mod4(highest_non_1mod4_idx)
  
  for power in count(1):
    composed = base_num * highest_non_1mod4_prime**power
    if composed > LIMIT:
      break
    this_total += total_for_1mod4_combo(composed, highest_non_1mod4_idx - 1)
  
  return this_total

power_configurations = (
  (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1),
  (3, 7), (7, 3),
  (1, 17), (17, 1),
  (2, 10), (10, 2),
  (52,)
)

def total_length_3_combo(p0, p1, p2, n): # return: (total, continue with this combo?)
  this_total = 0
  
  for prime_0_idx in range(n-1):
    for prime_1_idx in range(prime_0_idx + 1, n):
      num = nth_prime_1mod4(prime_0_idx)**p0 * nth_prime_1mod4(prime_1_idx)**p1 * nth_prime_1mod4(n)**p2
      
      if n % 100 == 0 and prime_0_idx == 0 and prime_1_idx == 1:
        print(n, num)
      
      if num > LIMIT:
        if prime_0_idx == 0 and prime_1_idx == 1:
          return this_total, False
        else:
          break
      
      this_total += total_for_1mod4_combo(num)
  
  return this_total, True

def total_length_2_combo(p0, p1, n): # return: (total, continue with this combo?)
  this_total = 0
  
  for prime_0_idx in range(1, n):
    num = nth_prime_1mod4(prime_0_idx)**p0 * nth_prime_1mod4(n)**p1
    
    if num > LIMIT:
      if prime_0_idx == 0:
        return this_total, False
      else:
        break
    
    this_total += total_for_1mod4_combo(num)
  
  return this_total, True

def total_length_1_combo(p, n): # return (total, continue with this combo?)
  num = nth_prime_1mod4(n)**p
  
  if num > LIMIT:
    return 0, False
  else:
    return total_for_1mod4_combo(num), True

if __name__ == '__main__':
  total = 0

  for power_config in power_configurations:
    for n in count(len(power_config) - 1):
      num = 1
      
      if len(power_config) == 3:
        p0, p1, p2 = power_config
        this_total, continue_combo = total_length_3_combo(p0, p1, p2, n)
      elif len(power_config) == 2:
        p0, p1 = power_config
        this_total, continue_combo = total_length_2_combo(p0, p1, n)
      else: # len is 1
        this_total, continue_combo = total_length_1_combo(power_config[0], n)
      
      total += this_total
      if not continue_combo:
        break
    
    print('Done power config {}: total = {}'.format(power_config, total))

  print(total)
