#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 38:

Take the number 192 and multiply it by each of 1, 2, and 3:

192 × 1 = 192
192 × 2 = 384
192 × 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product
of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645,
which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with
(1,2, ... , n) where n > 1?
"""

# Brute force

PANDIGITAL_SET = set(map(str, range(1, 10)))

def is_pandigital(s):
  return set(s) == PANDIGITAL_SET

largest = 0

for n in range(10000): # four digits is largest where digits(n) + digits(2*n) could conceivably be 9
  concat_product = ''
  m = 1
  
  while len(concat_product) < 9:
    concat_product += str(n * m)
    m += 1
  
  if len(concat_product) != 9 or not is_pandigital(concat_product):
    continue
  
  concat_product_num = int(concat_product)
  if concat_product_num > largest:
    largest = concat_product_num

print(largest)
