#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 32:

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example,
the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1
through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
"""

# Go through all multiplicands/multipliers with no repeated digits, check if total expression is pandigital

ALL_DIGITS = set(map(str, range(1, 10)))

products = set()

def is_pandigital(digits):
  if '0' in digits:
    return False
  
  for digit in ALL_DIGITS:
    if digits.count(digit) != 1:
      return False
  
  return True

# these maximum values are based on the fact that the total number of digits in a pandigital expression is 9
for a in range(1, 100):
  for b in range(1, 10000):
    product = a * b
    digits = str(a) + str(b) + str(product)
    if is_pandigital(digits):
      print('{} x {} = {}'.format(a, b, product))
      products.add(product)

print(sum(products))
