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
from math import sin, radians
from itertools import product


def gen_pqrs(n=360, m=180):
  p = q = r = 2
  s = n - p - q - r
  
  while s > 2:
    if p <= q <= r <= s and p < m and q < m and r < m and s < m:
      yield p, q, r, s
      
      if p != q and r != s:
        yield p, q, s, r
      
      if p != r and p != s and q != r and q != s:
        yield p, r, q, s
    
    s -= 1
    r += 1
    
    if r > s:
      r = 2
      q += 1
      s = n - p - q - r
      
      if q > s:
        q = 2
        p += 1
        s = n - p - q - r

total = 0

for p, q, r, s in gen_pqrs():
  if total % 1000 == 0:
    sys.stdout.write('\rtotal = {}, PQRS = {}'.format(total, (p, q, r, s)))
  
  side_lengths = set() # set of (QR, RS, PS) relative to PQ = 1
  
  for a, b in product(range(1, p), range(1, q)):
    # derive the rest of the angles from a and b
    h = p - a
    if h < 1: continue
    
    c = q - b
    if c < 1: continue
    
    x = 180 - a - b
    if x < 1: continue
      
    y = a + b
    
    g = 180 - h - y
    if g < 1: continue
    
    d = 180 - c - y
    if d < 1: continue
    
    f = s - g
    if f < 1: continue
    
    e = r - d
    if e < 1: continue
    
    #total += 1
    
    # convert all used in the side length calculations to radians
    arad = radians(a)
    brad = radians(b)
    crad = radians(c)
    drad = radians(d)
    frad = radians(f)
    grad = radians(g)
    
    sina = sin(arad)
    sind = sin(drad)
    
    # calculate side lengths; PQ = 1 assumed
    qr = sina / sind
    rs = (sina * sin(crad)) / (sin(frad) * sind)
    ps = sin(brad) / sin(grad)
    
    # check if any rotation is proportional
    if ((qr, rs, ps) not in side_lengths and (rs/qr, ps/qr, 1/qr) not in side_lengths and
        (ps/rs, 1/rs, qr/rs) not in side_lengths and (1/ps, qr/ps, rs/ps) not in side_lengths and
        (1/qr, ps/qr, rs/qr) not in side_lengths and (qr/rs, 1/rs, ps/rs) not in side_lengths and
        (rs/ps, qr/ps, 1/ps) not in side_lengths):
      # sys.stderr.write('P={}, Q={}, R={}, S={} | a={}, b={}, c={}, d={}, e={}, f={}, g={}, h={} | x={}, y={}\n'
      #   .format(p, q, r, s, a, b, c, d, e, f, g, h, x, y))
      side_lengths.add((qr, rs, ps))
    else:
      sys.stderr.write('REJECT: P={}, Q={}, R={}, S={} | a={}, b={}, c={}, d={}, e={}, f={}, g={}, h={} | x={}, y={}\n'
        .format(p, q, r, s, a, b, c, d, e, f, g, h, x, y))
  
  total += len(side_lengths)

print()
print(total)