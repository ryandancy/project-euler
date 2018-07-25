#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 62:

The cube, 41063625 (345^3), can be permuted to produce two other cubes: 56623104 (384^3) and 66430125 (405^3). In fact,
41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
"""

# Generate cubes, keep a dict of {sorted digits in cube: set of cubes with those digits}
# Once a digit has appeared 5 times, the minimum of the set of cubes with those digits is the result
# Runs in ~0.15 seconds

from itertools import count
from collections import defaultdict

digits = defaultdict(lambda: set())

for n in count(2):
  cube = n*n*n
  cube_digits = ''.join(sorted(str(cube)))
  
  digits[cube_digits].add(cube)
  
  if len(digits[cube_digits]) == 5:
    print(min(digits[cube_digits]))
    break
