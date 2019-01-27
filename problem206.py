#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 206:

Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0, where each "_" is a single digit.
"""

# least significant blank is 0, second least significant is 0, 4, or 8

from math import sqrt

for num in range(10**8):
  s = str(num)
  for second_last in '048':
    n = int('1{}2{}3{}4{}5{}6{}7{}8{}900'.format(*('0'*(7-len(s)) + s + second_last)))
    if int(sqrt(n))**2 == n:
      print(int(sqrt(n)))
      print(n)
      import sys
      sys.exit()
  if num % 100000 == 0:
    print(num)