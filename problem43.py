#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 43:

The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order,
but it also has a rather interesting sub-string divisibility property.

Let d(1) be the 1st digit, d(2) be the 2nd digit, and so on. In this way, we note the following:

d(2)d(3)d(4)=406 is divisible by 2
d(3)d(4)d(5)=063 is divisible by 3
d(4)d(5)d(6)=635 is divisible by 5
d(5)d(6)d(7)=357 is divisible by 7
d(6)d(7)d(8)=572 is divisible by 11
d(7)d(8)d(9)=728 is divisible by 13
d(8)d(9)d(10)=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.
"""

# Generate 0-9 pandigitals, check if they have this property
# Runs in ~5 seconds

from itertools import permutations

def divisible(n, d):
  return n % d == 0

def has_divisiblity_property(digits):
  # Using and-chain instead of all() for short-circuiting
  return (not digits.startswith('0')
    and divisible(int(digits[1:4]), 2)
    and divisible(int(digits[2:5]), 3)
    and divisible(int(digits[3:6]), 5)
    and divisible(int(digits[4:7]), 7)
    and divisible(int(digits[5:8]), 11)
    and divisible(int(digits[6:9]), 13)
    and divisible(int(digits[7:10]), 17))

print(sum(map(int, filter(has_divisiblity_property, map(''.join, permutations('1234567890', 10))))))
