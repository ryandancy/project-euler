#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 30:

Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

1634 = 1^4 + 6^4 + 3^4 + 4^4
8208 = 8^4 + 2^4 + 0^4 + 8^4
9474 = 9^4 + 4^4 + 7^4 + 4^4
As 1 = 1^4 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""

# Brute force, with updates to the console
# Will loop forever until killed by the user, but stabilizes to the maximum after ~3 seconds

from itertools import count
import sys

def is_digit_power_sum(n):
  return n == sum(int(m)**5 for m in str(n))

sum_ = 0
num_found = 0

try:
  for n in count(10):
    if n % 1000 == 0:
      # For efficiency: only write every 1000
      sys.stdout.write('\rFound: {} | Sum: {} | Checking: {}'.format(num_found, sum_, n))
      sys.stdout.flush()
    
    if is_digit_power_sum(n):
      sum_ += n
      num_found += 1
except KeyboardInterrupt:
  # the user exited: exit gracefully
  print('\nFinal sum:', sum_)
  sys.exit(0)
