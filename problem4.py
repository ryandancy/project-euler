#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 4:

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""

def is_palindrome(num):
  s = str(num)
  return s == s[::-1]

palindromes = [
  x * y
  for x in range(999, 99, -1)
  for y in range(x, 99, -1)
  if is_palindrome(x * y)
]

print(max(palindromes))
