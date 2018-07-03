#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 127:

The radical of n, rad(n), is the product of distinct prime factors of n. For example, 504 = 23 × 32 × 7, so rad(504) =
2 × 3 × 7 = 42.

We shall define the triplet of positive integers (a, b, c) to be an abc-hit if:

1. GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
2. a < b
3. a + b = c
4. rad(abc) < c

For example, (5, 27, 32) is an abc-hit, because:

1. GCD(5, 27) = GCD(5, 32) = GCD(27, 32) = 1
2. 5 < 27
3. 5 + 27 = 32
4. rad(4320) = 30 < 32

It turns out that abc-hits are quite rare and there are only thirty-one abc-hits for c < 1000, with ∑c = 12523.

Find ∑c for c < 120000.
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor
from math import sqrt, ceil, gcd
from functools import reduce, partial
import sys

memoized = {}
async def distinct_prime_factors(memoized_lock, n):
  await memoized_lock.acquire()
  if n in memoized:
    result = memoized[n]
    memoized_lock.release()
    return result
  memoized_lock.release()
  
  for divisor in range(2, int(sqrt(n)) + 1):
    other, remainder = divmod(n, divisor)
    if remainder == 0:
      result = await distinct_prime_factors(memoized_lock, divisor) | await distinct_prime_factors(memoized_lock, other)
      break
  else:
    result = {n}
  
  await memoized_lock.acquire()
  memoized[n] = result
  memoized_lock.release()
  
  return result

def rad_abc(af, bf, cf):
  return reduce(lambda x, y: x * y, af | bf | cf)

sum_c = 0
found = 0

async def check(memoized_lock, results_lock, low, high):
  print('New worker searching {} to {}'.format(low, high))
  
  sum_c_here = 0
  found_here = 0
  
  for c in range(low, high):
    for a in range(1, ceil(c/2)):
      b = c - a
      
      if gcd(a, b) != 1 or gcd(b, c) != 1 or gcd(a, c) != 1:
        continue
      
      af = await distinct_prime_factors(memoized_lock, a)
      bf = await distinct_prime_factors(memoized_lock, b)
      cf = await distinct_prime_factors(memoized_lock, c)
      
      if rad_abc(af, bf, cf) < c:
        sum_c_here += c
        found_here += 1
        print('Worker searching {} to {} found {}'.format(low, high, (a, b, c)))
  
  await results_lock.acquire()
  print('results lock acquired')
  global sum_c, found
  sum_c += sum_c_here
  found += found_here
  results_lock.release()
  print('results lock released')

loop = asyncio.get_event_loop()
memoized_lock = asyncio.Lock()
results_lock = asyncio.Lock()

try:
  executor = ProcessPoolExecutor(6)
  for n in range(0, 120000, 20000):
    asyncio.ensure_future(loop.run_in_executor(executor, partial(
      check, memoized_lock, results_lock, max(2, n), n + 20001)))
finally:
  loop.close()

print('\n')
print(sum_c)
