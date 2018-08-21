#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 99:

Comparing two numbers written in index form like 211 and 37 is not difficult, as any calculator would confirm that 2^11
= 2048 < 37 = 2187.

However, confirming that 632382^518061 > 519432^525806 would be much more difficult, as both numbers contain over three
million digits.

Using data/p099_base_exp.txt, a 22K text file containing one thousand lines with a base/exponent pair on each line,
determine which line number has the greatest numerical value.
"""

# Convert each to e^x, compare x
# e^x = a^b -> log(e^x) = log(a^b) -> x = b*log(a) since log(p^q) = q*log(p)
# Runs in ~0.1 seconds

from math import log

with open('data/p099_base_exp.txt', 'r') as data_file:
  pairs = [tuple(map(int, line.split(','))) for line in data_file]

largest_x = 0
largest_line = -1 # zero-indexed

for i, (base, exp) in enumerate(pairs):
  x = exp * log(base)
  if x > largest_x:
    largest_x = x
    largest_line = i

print('Largest natural exponent:', largest_x)
print('Zero-indexed line number:', largest_line)
print('One-indexed line number: ', largest_line + 1)
