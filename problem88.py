#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers, {a_1,
a_2, ..., a_k} is called a product-sum number: N = a_1 + a_2 + ... + a_k = a_1 × a_2 × ... × a_k.

For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.

For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number. The minimal
product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.

k=2: 4 = 2 × 2 = 2 + 2
k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2≤k≤6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in
the sum.

In fact, as the complete set of minimal product-sum numbers for 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2≤k≤12000?
"""

# Our algorithm is as follows:
# For each k from 2 to 12000, we compute the minimum product-sum number using 2 to k non-1 numbers in the list.
# For each number of non-1 numbers, we start with all 2s, increment the last number until their product >= their sum.
# When this occurs, we check if product == sum. We then increment the number before the most recently incremented
# number; if this would result in incrementing the -1st number, we exit. This process repeats until we increment the
# 0th number and find that it is too large. When incrementing a number, we also set each number after that to the
# incremented number.
# This solution runs in ~10 minutes.

def product(seq):
  result = 1
  for x in seq:
    result *= x
  return result

def minimal_product_sum_partial(k, non_1, min_found):
  ones = k - non_1
  numbers = [2] * non_1
  last_idx_incremented = 0
  first_overall = True
  
  while True:
    sum_ = sum(numbers) + ones
    prod = product(numbers)
    
    while prod < sum_ and (min_found is None or (sum_ < min_found and prod < min_found)):
      numbers[-1] += 1
      first_overall = False
      last_idx_incremented = non_1 - 1
      
      sum_ = sum(numbers) + ones
      prod = product(numbers)
    
    if sum_ == prod and (min_found is None or sum_ < min_found):
      min_found = sum_
    elif first_overall:
      raise StopIteration
    
    to_reset_to = last_idx_incremented - 1
    if to_reset_to < 0:
      return min_found
    
    numbers[to_reset_to] += 1
    for i in range(to_reset_to + 1, non_1):
      numbers[i] = numbers[to_reset_to]
    last_idx_incremented = to_reset_to

def minimal_product_sum(k):
  min_found = None
  try:
    for non_1 in range(2, k + 1):
      min_found = minimal_product_sum_partial(k, non_1, min_found)
  except StopIteration:
    pass
  return min_found

print(sum(set(map(minimal_product_sum, range(2, 12001)))))
