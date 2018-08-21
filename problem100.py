#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 100:

If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were taken
at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing
eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs in total, determine the number of blue
discs that the box would contain.
"""

# Works out to: find first integer x solution of x^2 - 2xy - y^2 - x + y = 0 where x + y > 10^12
# Apparently this works out as a recurrence relation: alternately (1 + 2y - x, y) and (x, 1 - y - 2x) starting at (0, 0)
# (thanks to https://math.stackexchange.com/questions/2869251/integer-points-on-a-hyperbola)
# Runs in ~0.1 seconds

def gen_solutions_one_spiral(up):
  x, y = (0, 0)
  while True:
    if up:
      y = 1 - y - 2*x
    else:
      x = 1 + 2*y - x
    up = not up
    yield (x, y)

def gen_solutions():
  yield (0, 0)
  
  spiral1 = gen_solutions_one_spiral(True)
  spiral2 = gen_solutions_one_spiral(False)
  
  while True:
    yield next(spiral1)
    yield next(spiral2)

MIN = 10**12
x, y = next((x, y) for x, y in gen_solutions() if x > 0 and y > 0 and x + y > MIN)
print(x)
