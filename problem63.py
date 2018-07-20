#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 63:

The 5-digit number, 16807=7^5, is also a fifth power. Similarly, the 9-digit number, 134217728=8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""

# It turns out that for any given base b, as the power n increases, b^n will either have n digits, or there will be no
# more n-digit nth powers for a larger n with the same base. Also, if there are no n-digit nth powers for a given base,
# then there will be no more n-digit nth powers for any greater base.
# This program runs in ~83ms.

from itertools import count

total = 0

for base in count(1):
  this_total = 0
  
  for power in count(1):
    power_digits = len(str(base ** power))
    
    if power_digits == power:
      this_total += 1
    else:
      break
  
  if this_total == 0:
    break
  
  total += this_total

print(total)
