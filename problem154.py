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


from sympy.ntheory import factorint
import sys


def get_powers(x, prime):
  powers = 0
  while x % prime**powers == 0:
    powers += 1
  return powers - 1


def add_dicts(d, addend):
  for key, val in addend.items():
    if key in d:
      d[key] += val
    else:
      d[key] = val


memoized = {}
def get_factorial_prime_factors(x):
  if x in memoized:
    return memoized[x]
  
  sum_factors = {}
  
  for y in range(1, x + 1):
    if y % 1000 == 0:
      sys.stdout.write('\rPrime factors generated up to {}'.format(y))
      sys.stdout.flush()
    
    add_dicts(sum_factors, factorint(y))
    
    # Fill in memoized to make it easier - this part should only be called for the original n
    memoized[y] = sum_factors.copy()
  
  # Not adding to memoized here because the previous if statement will have done so already
  return memoized[x]


# The multiplier is the number of times this partition appears in the layer
DISTINCT_TO_MULTIPLIER = {1: 1, 2: 3, 3: 6}
def get_multiplier(*partition):
  return DISTINCT_TO_MULTIPLIER[len(set(partition))]


def check_prime_factors(n_prime_factors, abc_prime_factors, powers_10_to_beat):
  delta_prime_factors = n_prime_factors - abc_prime_factors
  
  # check that we didn't exhaust any of the prime factors - that would cause a bad
  if delta_prime_factors.keys() != n_prime_factors.keys():
    return False
  
  # check that the powers of 10 are good
  powers_10 = min(delta_prime_factors[2], delta_prime_factors[5])
  return powers_10 <= powers_10_to_beat


def main(n=200000):
  print('Generating prime factors for n up to {}...'.format(n))
  n_prime_factors = get_factorial_prime_factors(n)
  total_powers_10 = min(n_prime_factors[2], n_prime_factors[5])
  print('\nAll factorial powers of 10 generated: total =', total_powers_10)
  
  sys.stderr.write(str(memoized[1]) + '\n')
  sys.stderr.flush()
  
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
    
    a_factorial_prime_factors = get_factorial_prime_factors(a)
    
    # the length 2 partition
    
    prime_factors = a_factorial_prime_factors + get_factorial_prime_factors(b) # 0! = 1, no 10-factors
    if check_prime_factors(n_prime_factors, prime_factors, powers_10_to_beat):
      sys.stderr.write('{} {} 0, {}\n'.format(a, b, 3 if a == b else 6))
      num_multiples_10_12 += 3 if a == b else 6 # faster than call to get_multiplier, I think
    
    # each length 3 partition
    for c in range(a, b // 2 + 1):
      new_b = b - c
      prime_factors = a_factorial_prime_factors + get_factorial_prime_factors(new_b) + get_factorial_prime_factors(c)
      if check_prime_factors(n_prime_factors, prime_factors, powers_10_to_beat):
        sys.stderr.write('{} {} {}, {}\n'.format(a, new_b, c, get_multiplier(a, new_b, c)))
        num_multiples_10_12 += get_multiplier(a, new_b, c)
  
  print('\nTotal number of multiples of 10^12 found:', num_multiples_10_12)


if __name__ == '__main__':
  main()
