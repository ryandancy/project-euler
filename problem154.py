#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 154:

A triangular pyramid is constructed using spherical balls so that each ball rests on exactly three balls of the next
lower level.

Then, we calculate the number of paths leading from the apex to each position:

A path starts at the apex and progresses downwards to any of the three spheres directly below the current position.

Consequently, the number of paths to reach a certain position is the sum of the numbers immediately above it (depending
on the position, there are up to three numbers above it).

The result is Pascal's pyramid and the numbers at each level n are the coefficients of the trinomial expansion
(x + y + z)^n.

How many coefficients in the expansion of (x + y + z)^200000 are multiples of 10^12?
"""

# KEEP TRACK OF 2 AND 5 so that if a has 2, b has 5, that combines to a 10


import sys


def get_powers(x, prime):
  powers = 0
  while x % prime**powers == 0:
    powers += 1
  return powers - 1


memoized = {}
def get_factorial_2_5_factors(x):
  if x in memoized:
    return memoized[x]
  
  sum_2 = 0
  sum_5 = 0
  
  for y in range(1, x + 1):
    sum_2 += get_powers(y, 2)
    sum_5 += get_powers(y, 5)
    
    # Fill in memoized to make it easier - this part should only be called for the original n
    memoized[y] = (sum_2, sum_5)
  
  # Not adding to memoized here because the previous if statement will have done so already
  return memoized[x]


# The multiplier is the number of times this partition appears in the layer
DISTINCT_TO_MULTIPLIER = {1: 1, 2: 3, 3: 6}
def get_multiplier(*partition):
  return DISTINCT_TO_MULTIPLIER[len(set(partition))]


def main(n=200000):
  print('Generating 2- and 5-factors for n up to {}...'.format(n))
  n_2_5_factors = get_factorial_2_5_factors(n)
  total_powers_10 = min(n_2_5_factors)
  print('All factorial powers of 10 generated: total =', total_powers_10)
  
  powers_10_to_beat = total_powers_10 - 12
  
  num_multiples_10_12 = 0
  
  # there are no length 1 partitions because it'll be n!/n! = 1, not divisible by 10^12
  
  print('Checking partitions...')
  
  for a in range(1, n // 2 + 1):
    if a % 10 == 0:
      sys.stdout.write('\rChecked: a = {} ({:.2f}%) | Multiples of 10^12 found: {}'.format(
        a, (a / (n // 2)) * 100, num_multiples_10_12))
      sys.stdout.flush()
    
    b = n - a
    
    a_2_factors, a_5_factors = get_factorial_2_5_factors(a)
    
    # the length 2 partition
    
    b_2_factors, b_5_factors = get_factorial_2_5_factors(b)
    ab_10_factors = min(a_2_factors + b_2_factors, a_5_factors + b_5_factors)
    if ab_10_factors <= powers_10_to_beat:
      num_multiples_10_12 += 3 if a == b else 6 # faster than call to get_multiplier, I think
    
    # each length 3 partition
    for c in range(a, b // 2 + 1):
      new_b = b - c
      
      new_b_2_factors, new_b_5_factors = get_factorial_2_5_factors(new_b)
      c_2_factors, c_5_factors = get_factorial_2_5_factors(c)
      abc_10_factors = min(a_2_factors + new_b_2_factors + c_2_factors, a_5_factors + new_b_5_factors + c_5_factors)
      
      if abc_10_factors <= powers_10_to_beat:
        num_multiples_10_12 += get_multiplier(a, new_b, c)
  
  print('\nTotal number of multiples of 10^12 found:', num_multiples_10_12)


if __name__ == '__main__':
  main()
