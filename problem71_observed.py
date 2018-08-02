#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the brute-force method used to get the exact answer to problem 71. It was observed that all the answers had
# a numerator between 427000 and 429000 and a denominator between 996000 and 1000000, so this program checks all of
# them. It finds the real answer in ~7 seconds.

# Checking 427000 to 429000 over 996000 to 1000000

from math import gcd

min_n = -1
min_d = 1

for n in range(427000, 429001):
  print(n, ' | min = ', min_n, '/', min_d, sep='')
  
  for d in range(996000, 1000000):
    if gcd(n, d) != 1:
      continue
    
    if 7*n < 3*d and n*min_d > d*min_n:
      min_n = n
      min_d = d

print(min_n)
