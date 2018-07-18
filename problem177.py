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
Let a quadrilateral to be considered be PQRS. Let the corner angles RPQ = a, PQS = b, SQR = c, QRP = d, PRS = e, RSQ =
f, QSP = g, and SPR = h; in other words, the corner angles are assigned to a through h clockwise starting at RPQ. Thus
P = a + h, Q = b + c, R = d + e, and S = f + g.

This program generates valid integral values for P, Q, R, S, and a, derives the rest of the angles, and checks that all
the derived angles are valid and that the quadrilateral described by them is not similar to any other quadrilateral.

First, let us deal with the question of similarity. If two quadrilaterals ABCD and PQRS are similar, then both (a)
corresponding angles are equal (i.e. A=P, B=Q, C=R, and D=S), and (b) corresponding sides are proportional (i.e. AB/PQ
= BC/QR = CD/RS = DA/SP). It can be proven using the sine law that if corresponding corner angles are equal, then
corresponding sides are proportional; thus similarity can be shown using the angles and corner angles alone.

As well, similar quadrilaterals may need to be rotated and/or reflected to conform to each other; to accommodate this,
all of the following tuples of corner angles are considered equivalent for the purpose of similarity:

(h, a, b, c, d, e, f, g)
(b, c, d, e, f, g, h, a)
(d, e, f, g, h, a, b, c)
(f, g, h, a, b, c, d, e)
(g, f, e, d, c, b, a, h)
(a, h, g, f, e, d, c, b)
(c, b, a, h, g, f, e, d)
(e, d, c, b, a, h, g, f)

Note, however, that pairs of corner angles such as (b, c) that both correspond to the same angle of the quadrilateral
(such as Q) cannot be broken apart without similarity being lost; thus e.g. (c, d, e, f, g, h, a, b) is not equivalent
for the purposes of similarity.

Secondly, I will demonstrate how all the other corner angles in an arbitrary convex quadrilateral may be derived from
the four quadrilateral angles P, Q, R, and S and one corner angle a.

Let the intersection of the diagonals PR and SQ be X; let PXQ = SXR = x and PXS = QXR = y. The corner angles c through h
(as well as x and y) may be trivially derived from P, Q, R, S, a, and b:

h = P - a
c = Q - b

x = 180 - a - b
y = 180 - x
  = a + b

g = 180 - h - y
  = 180 - (P - a) - a - b
  = 180 - b - P

d = 180 - c - y
  = 180 - (Q - b) - a - b
  = 180 - a - Q

e = R - d
  = R + a + Q - 180
f = S - g
  = S + b + P - 180

Not so trivial, however, is deriving b from a. This can be done graphically, however, if one follows the following
procedure on a Cartesian plane:

1. Place a point P(0, 0).
2. Draw a ray PA on the X axis going rightwards (towards positive X) and emanating from P.
3. Draw a ray PB emanating from P above the X axis such that angle BPA = angle P.
4. Draw a ray PC emanating from P above the X axis such that angle CPA = angle a.
5. Place a point Q on PX. The placement of Q does not matter as long as it is distinct from P and on PX.
6. Draw a ray QD emanating from Q above the X axis such that angle DQP = angle Q.
7. Where QD intersects PC, place point R.
8. Draw a ray RE emanating from R going leftwards (towards negative X) such that angle ERQ = angle R.
9. Where RE intersects PB, place point S. Angle PSR = angle S.
10. Draw the line SQ. Angle SQP = angle b.

When this procedure is translated into analytical geometry, the following general formula for b is obtained:

b = -arctan((z tan(P))/(z - 1)), where z = (tan(a)tan(Q) + tan(Q)tan(R+Q)) / ((tan(a) + tan(Q))(tan(P) + tan(R+Q)))

See https://www.desmos.com/calculator/kdblrrblo for an interactive demonstration.

However, tan(90°) is undefined. There are four special cases to work around this:

If P = 90°, then:  (https://www.desmos.com/calculator/vnwqd8numc)
b = -arctan(-(tan(a)tan(Q) + tan(Q)tan(R+Q))/(tan(a) + tan(Q)))

If Q = 90°, then:  (https://www.desmos.com/calculator/qotxyb3fjp)
b = -arctan((z tan(P))/(z - 1)), where z = (tan(a) + tan(R+90°)) / (tan(P) + tan(R+90°))

If P = Q = 90°, then:  (https://www.desmos.com/calculator/x3bggvlb2c)
b = -arctan(-tan(a) - tan(R+90°))

If a = 90°, then:  (https://www.desmos.com/calculator/mirqlduhwv)
b = -arctan((z tan(P))/(z - 1)), where z = tan(Q) / (tan(P) + tan(R+Q))

The case R+Q = 90° is impossible when P, Q, R, and S are generated as in this program.

A quirk of these deriving functions is that when b is obtuse (90 < b < 180), it will be returned as b - 180 (such that
-90 < b < 0). This is worked around by adding 180 to b when it is less than 0.

This program works by generating every distinct value of P, Q, R, and S such that 2 <= P <= Q <= R <= S < 180. It also
generates permutations of P, Q, R, S that cannot be read forwards or backwards from any point in the permutation to read
PQRS (i.e. if P != Q and R != S, (P, Q, S, R) is generated; and if P != R and P != S and Q != R and Q != S, (P, R, Q, S)
is generated); any other permutation would be similar to PQRS.

For every generated value of P, Q, R, and S, the program then loops through all potential values of a (1 <= a < P). It
then calculates b and checks that it is an integer (within a tolerance of 10^-9) and between 0 and 180. If this is true
and b is valid, the program then calculates the values of corner angles c through h, checks their validity, and then
checks that the quadrilateral is not similar to any other quadrilateral with the same values of P, Q, R, and S using the
method established previously. If so, the total number of non-similar integer angled quadrilaterals is incremented.

This program finds the correct value in approximately 45 seconds.
'''

import sys
from math import tan, atan, radians, degrees

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
  # return round(angle) too so we don't have to recalculate it
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

total = 0
old_p = 0

for p, q, r, s in gen_pqrs():
  if p != old_p:
    # status update to the console
    sys.stdout.write('\rChecked P = {} ({:.2f}% done) | Total = {}'.format(p, (p / 90) * 100, total))
    old_p = p
  
  distincts = set()
  
  for a in range(1, p):
    b = get_b(a, p, q, r)
    
    if b < 0:
      # if b is obtuse, get_b will return it minus 180 for some reason; counteract this
      b += 180
    
    b, integral = is_integral(b)
    if not integral or b <= 0 or b >= 180:
      continue
    
    h = p - a
    if h < 1: continue
    
    c = q - b
    if c < 1: continue
    
    g = 180 - b - p
    if g < 1: continue
    
    d = 180 - a - q
    if d < 1: continue
    
    f = s + b + p - 180
    if f < 1 or f >= 180: continue
    
    e = r + a + q - 180
    if e < 1 or e >= 180: continue
    
    if is_distinct(distincts, a, b, c, d, e, f, g, h):
      distincts.add((h, a, b, c, d, e, f, g)) # odd order is implementation detail in is_distinct
  
  total += len(distincts)

print()
print('Final total:', total)
