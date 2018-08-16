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

import sys
sys.setrecursionlimit(12500)

def product(seq):
  result = 1
  for x in seq:
    result *= x
  return result

def minimal_product_sum(k, add=[]):
  if not add:
    print(k)
  
  if k == 1:
    s = [*add, 2]
    while sum(s) > product(s):
      s[-1] += 1
    return s
  
  if k == 2:
    last = max(add[-1], 2) if add else 2
  else:
    last = add[-1] if add else 1
  
  s = [*add, last]
  minimal = 10**10
  minimal_s = None
  lastn = 10**10
  
  while True:
    new = minimal_product_sum(k - 1, s)
    if new is None:
      break
    
    n = sum(new)
    
    if n == product(new) and n < minimal:
      minimal = n
      minimal_s = new
    
    if n > lastn:
      break
    lastn = n
    
    s[-1] += 1
  
  return minimal_s

print(sum(set(map(sum, map(minimal_product_sum, range(2, 12001))))))
