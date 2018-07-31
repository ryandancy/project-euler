#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A row measuring seven units in length has red blocks with a minimum length of three units placed on it, such that any
two red blocks (which are allowed to be different lengths) are separated by at least one black square. There are exactly
seventeen ways of doing this.

How many ways can a row measuring fifty units in length be filled?
"""

# A recursive solution with memoization, runs in less than 0.1 seconds

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

print(num_fills(3, 50))
