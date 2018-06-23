#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 26:

A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10
are given:

1/2 = 0.5
1/3 = 0.(3)
1/4 = 0.25
1/5 = 0.2
1/6 = 0.1(6)
1/7 = 0.(142857)
1/8 = 0.125
1/9 = 0.(1)
1/10 = 0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring
cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""

from collections import defaultdict

def recurring_cycle_length(d):
  # Long division algorithm keeping track of remainders previously seen
  # If a remainder repeats, the cycle has started to repeat and we return
  
  remainders_seen = set()
  cycle_length = 0
  
  current_divisor = 1
  while True:
    quotient, remainder = divmod(current_divisor, d)
    
    if quotient == 0:
      # too small to divide once: add a zero in the result
      current_divisor *= 10
      
      if cycle_length > 0:
        # it's a zero in a cycle, not at the start
        cycle_length += 1
      
      continue
    
    if remainder == 0:
      # it divides evenly
      return 0
    
    if remainder in remainders_seen:
      # this cycle is now repeating
      return cycle_length
    
    remainders_seen.add(remainder)
    current_divisor = remainder * 10
    cycle_length += 1

print(max(range(2, 1000), key=recurring_cycle_length))
