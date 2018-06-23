#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 28:

Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
"""

# The sequence of numbers on the diagonals is the following:
# 1, 3, 5, 7, 9, 13, 17, 21, 25, 31, 37, 43, 49, ...
# Let d(n) be the nth number in this sequence.
# After d(1) = 1:
#  d(n) = d(n-1) + 2 for 2 <= n <= 5
#  d(n) = d(n-1) + 4 for 6 <= n <= 9
#  d(n) = d(n-1) + 6 for 10 <= n <= 13, etc.
# Also, the number of diagonal numbers in an n×n spiral is 2(n-1) + 1 = 2n - 1.

n = 1001

def diagonals(n):
  yield 1
  
  i = 0
  adding = 2
  current = 1
  
  while i < n - 1:
    current += adding
    yield current
    
    i += 1
    if i % 4 == 0:
      adding += 2

print(sum(diagonals(2*n - 1)))
