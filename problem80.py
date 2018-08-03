#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 80:

It is well known that if the square root of a natural number is not an integer, then it is irrational. The decimal
expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal digits
for all the irrational square roots.
"""

# Uses the "digit-by-digit" square root calculation method iterated 100 times for each number in [1, 100]
# If the algorithm terminates, 0 is returned as the digit sum
# (https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Decimal_(base_10))
# Runs in ~0.1 seconds

def sqrt_digit_sum(n): # 0 < n < 100
  found = 0
  sum_ = 0
  current = n
  
  for _ in range(100):
    found10 = 10*found
    found20 = 2*found10
    
    x = 0
    while x * (found20 + x) <= current:
      x += 1
    x -= 1
    y = x * (found20 + x)
    
    sum_ += x
    found = found10 + x
    current = (current - y) * 100
    
    if current == 0:
      # not irrational
      return 0
  
  return sum_

print(sum(map(sqrt_digit_sum, range(1, 100))))
