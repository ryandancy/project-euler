#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 23:

A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the
sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum
exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as
the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is
known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
"""

# First: find all abundant numbers <= 28123

import math
import itertools

def divisors(n):
  divisors = {1}
  sqrt = math.sqrt(n)
  
  for divisor in range(2, int(sqrt) + 1):
    other_divisor, remainder = divmod(n, divisor)
    if remainder == 0:
      divisors.update({divisor, other_divisor})
  
  return divisors

abundants = [n for n in range(2, 28124) if sum(divisors(n)) > n]

# Next: a sort of Sieve of Eratosthenes for all combinations of abundants
is_non_abundant = [True for x in range(28123)] # index + 1 = number, value = non abundant

for abundant_combo in itertools.combinations_with_replacement(abundants, 2):
  abundant_sum = sum(abundant_combo)
  if abundant_sum <= len(is_non_abundant):
    is_non_abundant[abundant_sum-1] = False

# Finally: sum up the remaining True indicies
print(sum(idx + 1 for idx, non_abundant in enumerate(is_non_abundant) if non_abundant))
