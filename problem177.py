#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 177:

Let ABCD be a convex quadrilateral, with diagonals AC and BD. At each vertex the diagonal makes an angle with each of
the two sides, creating eight corner angles.

For example, at vertex A, the two angles are CAD, CAB.

We call such a quadrilateral for which all eight corner angles have integer values when measured in degrees an "integer
angled quadrilateral". An example of an integer angled quadrilateral is a square, where all eight corner angles are 45°.
Another example is given by DAC = 20°, BAC = 60°, ABD = 50°, CBD = 30°, BCA = 40°, DCA = 30°, CDB = 80°, ADB = 50°.

What is the total number of non-similar integer angled quadrilaterals?

Note: In your calculations you may assume that a calculated angle is integral if it is within a tolerance of 10^-9 of an
integer value.
"""


import sys

MAX = 180

a = d = e = 1
y = 2
x = MAX - a - d
h = MAX - y - e

total = 0

while a <= MAX - 3:
  sys.stdout.write('\ra = {}, total = {}'.format(a, total))
  
  while x >= 2:
    while y + h >= x:
      while h >= 1:
        if x + d >= y and MAX - e - d > 2 and MAX - a - h > 2:
          #sys.stderr.write(str((a, x, d, e, y, h)) + '\n')
          total += 1
        h -= 1
        y += 1
      
      e += 1
      y = 2
      h = MAX - y - e
    
    d += 1
    x -= 1
    e = 1
  
  a += 1
  d = e = 1
  y = 2
  x = MAX - a - d
  h = MAX - y - e

print()
print(total)
