#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 243:

A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d−1 proper fractions; for example, with d = 12:

1/12, 2/12, 3/12, 4/12, 5/12, 6/12, 7/12, 8/12, 9/12, 10/12, 11/12.

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), to be the ratio of its proper fractions that are
resilient; for example, R(12) = 4/11.
In fact, d = 12 is the smallest denominator having a resilience R(d) < 4/10.

Find the smallest denominator d, having a resilience R(d) < 15499/94744 .
"""

'''
Note that the number of reducible fractions for a given denominator is directly related to the number of distinct prime
factors of a given number. Specifically, the number of resilient fractions for a given denominator d is the number of
integers that remain when every integer 1 <= n < d divisible by one or more of the prime factors of d is removed from
the set {1, 2, ..., d - 1}. This could be directly calculated using a sieve, but that algorithm would have O(n) space
complexity and would eat up too much memory for large d. However, the combinations can also be calculated by starting
with d, subtracting d / f for each distinct prime factor f, adding d / (f_0 * f_1) for each pair of distinct prime
factors f_0 and f_1, and continuing until all combinations of d - 1 prime factors are used. This is how resilience is
calculated.

Also note that numbers with extremely low resiliences will have a large number of distinct prime factors. However, the
optimal denominator for a certain resilience may contain non-distinct prime factors; see d = 12 = 2*2*3, optimal for
R(d) < 4/10. Thus, the optimal denominator is found by adding prime factors to increasing lists of distinct prime
factors and finding the lowest denominator for each list of added prime factors.

This program runs in approximately 2 seconds.
'''


from fractions import Fraction
from itertools import combinations, count
from functools import reduce
import operator


RESILIENCE_LIMIT = Fraction(15499, 94744)


def resilience(factors):
  # Compute the resilience (and the number) described by the prime factors `factors`, expanded like [2, 2, 3] for 12
  
  denom = reduce(operator.mul, factors)
  
  num_resil = denom - 1
  add = False
  
  for i in range(1, len(factors)):
    for combo in set(combinations(set(factors), i)):
      combo_num = denom // reduce(operator.mul, combo) - 1 # subtracting 1 to exclude denom
      if add:
        num_resil += combo_num
      else:
        num_resil -= combo_num
    add = not add
  
  resil = Fraction(num_resil, denom - 1)
  
  return denom, resil


def gen_prime_lists():
  # Generate successive lists of primes: [2], [2, 3], [2, 3, 5], [2, 3, 5, 7], ...
  primes = []
  for n in count(2):
    for prime in primes:
      if n % prime == 0:
        break
    else:
      primes.append(n)
      yield primes


def find_first(add):
  # Find the first set of factors with resilience below the limit, adding `add` to each set of prime factors
  for prime_list in gen_prime_lists():
    denom, resil = resilience(prime_list + add)
    if resil < RESILIENCE_LIMIT:
      return denom


def optimize(prime_list, add=[]):
  factors = add[:]
  
  if len(prime_list) == 1:
    func = lambda _, factors: find_first(factors)
  else:
    func = optimize
  
  truncated_prime_list = prime_list[:-1]
  denom = func(truncated_prime_list, factors)
  old_denom = denom + 1
  
  while denom < old_denom:
    factors.append(prime_list[-1])
    old_denom = denom
    denom = func(truncated_prime_list, factors)
  
  return old_denom


if __name__ == '__main__':
  lowest_denom = -1
  
  for prime_list in gen_prime_lists():
    print('Checking prime list {}, current lowest = {}'
          .format(prime_list, 'infinity' if lowest_denom == -1 else lowest_denom))
    
    if lowest_denom > 0 and reduce(operator.mul, prime_list) > lowest_denom:
      print(lowest_denom)
      break
    else:
      denom = optimize(prime_list)
      if lowest_denom < 0 or denom < lowest_denom:
        lowest_denom = denom
