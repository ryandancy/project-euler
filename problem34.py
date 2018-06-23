#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 34:

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.
"""

# No upper bound, so this is done with updates to the console

from math import factorial
from itertools import count
import sys

factorials = {str(n): factorial(n) for n in range(10)}

sum_ = 0
numbers = set()

try:
  for n in count(10):
    if n == sum(map(lambda digit: factorials[digit], str(n))):
      sum_ += n
      numbers.add(n)
    
    if n % 1000 == 0:
      sys.stdout.write('\rFound: {} | Sum: {} | Checking: {}'.format(numbers, sum_, n))
      sys.stdout.flush()
except KeyboardInterrupt:
  # exit gracefully
  print('\nFinal sum:', sum_)
  sys.exit(0)
