#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 115:

A row measuring n units in length has red blocks with a minimum length of m units placed on it, such that any two red
blocks (which are allowed to be different lengths) are separated by at least one black square.

Let the fill-count function, F(m, n), represent the number of ways that a row can be filled.

For example, F(3, 29) = 673135 and F(3, 30) = 1089155.

That is, for m = 3, it can be seen that n = 30 is the smallest value for which the fill-count function first exceeds one
million.

In the same way, for m = 10, it can be verified that F(10, 56) = 880711 and F(10, 57) = 1148904, so n = 57 is the least
value for which the fill-count function first exceeds one million.

For m = 50, find the least value of n for which the fill-count function first exceeds one million.
"""

# Using the same fill-count function as in problem 114, runs in ~0.2 seconds.

from itertools import count

memoized = {}
def num_fills(min_block_size, length, base=1):
  result = base # 1 for the no-blocks case if this isn't a recurse
  
  if min_block_size > length:
    # skip memoization when empty's the only case
    return result
  
  if (min_block_size, length) in memoized:
    return memoized[(min_block_size, length)]
  
  for block_size in range(min_block_size, length + 1):
    for shift in range(length - block_size + 1):
      result += num_fills(min_block_size, shift - 1, 0) + 1
  
  memoized[(min_block_size, length)] = result
  return result

for n in count(51):
  if num_fills(50, n) > 1000000:
    print(n)
    break
