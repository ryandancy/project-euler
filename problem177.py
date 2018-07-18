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

'''
This program does not work, but it *should*.

Let each quadrilateral be PQRS. This program generates every P, Q, R, and S which are not rotations nor reflections of
each other, to eliminate those that are similar based on angles.
'''

import sys
from math import tan, atan, radians, degrees, ceil

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

def get_b(a, p, q, r):
  # https://www.desmos.com/calculator/kdblrrbloa
  # For P=90: https://www.desmos.com/calculator/vnwqd8numc
  # For Q=90: https://www.desmos.com/calculator/qotxyb3fjp
  # For P=Q=90: https://www.desmos.com/calculator/x3bggvlb2c
  # For a=90: https://www.desmos.com/calculator/mirqlduhwv
  
  if p == 90:
    if q == 90:
      return degrees(-atan(-tan(radians(a)) - tan(radians(r + 90))))
    else:
      ra, rr, rq = radians(a), radians(r), radians(q)
      
      tana = tan(ra)
      tanq = tan(rq)
      tanrq = tan(rr + rq)
      
      m = -(tana*tanq + tanq*tanrq) / (tana + tanq)
      
      return degrees(-atan(m))
  elif q == 90:
    rp, ra, rr90 = radians(p), radians(a), radians(r + 90)
    
    tanp = tan(rp)
    tana = tan(ra)
    tanr90 = tan(rr90)
    
    z = (tana + tanr90) / (tanp + tanr90)
    m = (z * tanp) / (z - 1)
    
    return degrees(-atan(m))
  elif a == 90:
    rp, rq, rr = radians(p), radians(q), radians(r)
    
    tanp = tan(rp)
    tanq = tan(rq)
    tanrq = tan(rr + rq)
    
    z = tanq / (tanp + tanrq)
    m = (z * tanp) / (z - 1)
    
    return degrees(-atan(m))
  
  ra, rp, rq, rr = radians(a), radians(p), radians(q), radians(r)
  
  tana = tan(ra)
  tanq = tan(rq)
  tanp = tan(rp)
  tanrq = tan(rr + rq)
  
  z = (tana*tanq + tanq*tanrq) / ((tana + tanq) * (tanp + tanrq))
  
  try:
    m = (z * tanp) / (z - 1)
    return degrees(-atan(m))
  except ZeroDivisionError:
    # Edge case: z = 1 and SQ's slope is undefined (vertical line)
    # then b = 90
    return 90

INTEGRAL_TOLERANCE = 10**-9

def is_integral(angle):
  # within 10^-9 of an integral value
  # returns round(angle) too so we don't have to recalculate it
  rounded = round(angle)
  return rounded, abs(angle - rounded) <= INTEGRAL_TOLERANCE

def is_distinct(distincts, a, b, c, d, e, f, g, h):
  return all(angles not in distincts for angles in [
    (h, a, b, c, d, e, f, g),
    (b, c, d, e, f, g, h, a),
    (d, e, f, g, h, a, b, c),
    (f, g, h, a, b, c, d, e),
    # and reversed:
    (g, f, e, d, c, b, a, h),
    (a, h, g, f, e, d, c, b),
    (c, b, a, h, g, f, e, d),
    (e, d, c, b, a, h, g, f),
  ])

print(get_b(30, 70, 120, 90)) # 71.494428717336 good
print(get_b(76, 103, 33, 90)) # 13.492999251890225 good
print(get_b(49, 110, 90, 102)) # 43.85130532847164 good
print(get_b(45, 90, 102, 34)) # 2.494967342781688 good
print(get_b(44, 90, 90, 102)) # 49.67807796118421 good
print(get_b(90, 126, 84, 21)) # 41.84593332780234 good

total = 0
old_p = 0

for p, q, r, s in gen_pqrs():
  if p != old_p:
    sys.stdout.write('\rtotal = {}, PQRS = {} ({:.2f}%)'.format(total, (p, q, r, s), (p / 90) * 100))
    old_p = p
  
  distincts = set()
  
  for a in range(1, p):
    b = get_b(a, p, q, r)
    b, integral = is_integral(b)
    if not integral or b <= 0 or b >= 180:
      continue
    
    h = p - a
    if h < 1: continue
    
    c = p - b
    if c < 1: continue
    
    g = 180 - b - p
    if g < 1: continue
    
    d = 180 - a - p
    if d < 1: continue
    
    f = s + b + p - 180
    if f < 1 or f >= 180: continue
    
    e = r + a + p - 180
    if e < 1 or e >= 180: continue
    
    if is_distinct(distincts, a, b, c, d, e, f, g, h):
      distincts.add((h, a, b, c, d, e, f, g)) # odd order is implementation detail in is_distinct
  
  total += len(distincts)

print()
print(total)
