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


'''
The value of a coefficient in a k-nomial expansion -- the expansion of (x_1 + x_2 + ... + x_k)^n -- is equal to
n! / (a_1! * a_2! * ... * a_k!) where a_1 + a_2 + ... + a_k = n. Specifically, the value of any coefficient in the
200000th row of Pascal's pyramid is 200000! / (a! * b! * c!) where a + b + c = 200000.

Now, note that we are looking only for the coefficients which are divisible by 10^12. This is the case if the number of
"10-factors" (integer x where 10^x * y = z for some integer y and the given integer z) in 200000! minus those in
a! * b! * c! is greater than or equal to 12. Since 10 = 5*2, the number of 10-factors in a number is equal the the
smaller of its number of 5-factors and 2-factors; thus a coefficient for given integers a, b, c where a + b + c =
200000 is divisible by 10^12 if the smaller of the number of 5-factors and 2-factors in 200000! minus the smaller of
the total number of 2-factors in a! * b! * c! and the total number of 5-factors in that number is greater than or equal
to 12.

Now, the nth layer of Pascal's pyramid contains all coefficients n!/(a!*b!*c!) where the integers a + b + c = n -- the
coefficients for all compositions of n of length 3 or fewer. However, it is computationally simpler to simply calculate
the partitions of n of length 3 or fewer and count the number of times that that partition appears in the nth layer of
Pascal's pyramid -- i.e., how many distinct ways that combination may be arranged. This can be calculated by determining
the number of distinct elements that exist in the partition. With all 3 elements distinct, the partition appears 6
times; with 2 distinct elements, it appears 3 times; and with only 1 distinct element (all elements the same), the
partition appears only once. This is used to simplify computation.

This program begins by calculating the number of 2-factors and 5-factors in the factorial of every number up to
200000 and storing for future reference. It then iterates through all distinct length 2 partitions of 200000,
calculating the total number of 2-factors and 5-factors and comparing that minimum to that of 200000; for each length
2 partition, the length 3 partitions are also generated and checked.

This program finds the correct answer in approximately 1 hour.
'''


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
  print('Generating 2-factors and 5-factors for n up to {}...'.format(n))
  n_2_factors, n_5_factors = get_factorial_2_5_factors(n)
  print('All factorial powers of 10 generated: total 2-factors = {}, total 5-factors = {}'
        .format(n_2_factors, n_5_factors))
  
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
    ab_2_factors, ab_5_factors = a_2_factors + b_2_factors, a_5_factors + b_5_factors
    
    if min(n_2_factors - ab_2_factors, n_5_factors - ab_5_factors) >= 12:
      num_multiples_10_12 += 3 if a == b else 6 # faster than call to get_multiplier, I think
    
    # each length 3 partition
    for c in range(a, b // 2 + 1):
      new_b = b - c
      
      new_b_2_factors, new_b_5_factors = get_factorial_2_5_factors(new_b)
      c_2_factors, c_5_factors = get_factorial_2_5_factors(c)
      
      abc_2_factors = a_2_factors + new_b_2_factors + c_2_factors
      abc_5_factors = a_5_factors + new_b_5_factors + c_5_factors
      
      if min(n_2_factors - abc_2_factors, n_5_factors - abc_5_factors) >= 12:
        num_multiples_10_12 += get_multiplier(a, new_b, c)
  
  print('\nTotal number of multiples of 10^12 found:', num_multiples_10_12)


if __name__ == '__main__':
  main()
