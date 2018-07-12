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

# Runs out of memory at ~15%

import sys

def gen_abcd(total=180):
  a = b = c = 1
  d = total - 3
  
  while True:
    d -= 1
    c += 1
    if d < 1:
      c = 1
      b += 1
      d = total - a - b - c
      sys.stdout.write('\ra = {}, b = {} ({:.2f}%) | Similars: {}'
        .format(a, b, a / (total - 3) * 100 + b / (total - 3), len(similars)))
      if d < 1:
        b = 1
        a += 1
        d = total - a - b - c
        if d < 1:
          return
    yield a, b, c, d

similars = set()

for a, b, c, d in gen_abcd():
  ef = a + b
  gh = c + d
  for e in range(1, ef):
    f = ef - e
    for g in range(1, gh):
      h = gh - g
      if (a, b + c, d, e, f + g, h) not in similars and (c, d + e, f, g, a + h, b) not in similars:
        similars.add((a, b + c, d, e, f + g, h))
        sys.stderr.write('a={}, b={}, c={}, d={}, e={}, f={}, g={}, h={}; angles: {}\n'
                         .format(a, b, c, d, e, f, g, h, (a, b + c, d, e, f + g, h)))

print()
print(len(similars))

#print(sum((x - 1)**2 * (179 - x)**2 for x in range(1, 180)))
