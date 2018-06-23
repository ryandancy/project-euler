#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 36:

The decimal number, 585 = 1001001001_2 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""

def is_palindrome_both(n):
  decimal = str(n)
  binary = bin(n)[2:]
  return decimal == decimal[::-1] and binary == binary[::-1]

sum_ = 0

for n in range(1, 1000000):
  if is_palindrome_both(n):
    sum_ += n

print(sum_)
