#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 450:

A hypocycloid is the curve drawn by a point on a small circle rolling inside a larger circle. The parametric equations
of a hypocycloid centered at the origin, and starting at the right most point is given by:

x(t) = (R−r)cos(t)+rcos(t(R−r)/r)
y(t) = (R−r)sin(t)−rsin(t(R−r)/r)

Where R is the radius of the large circle and r the radius of the small circle.

Let C(R,r) be the set of distinct points with integer coordinates on the hypocycloid with radius R and r and for which
there is a corresponding value of t such that sin(t) and cos(t) are rational numbers.

Let S(R,r)=∑_{(x,y)∈C(R,r)} |x|+|y| be the sum of the absolute values of the x and y coordinates of the points in
C(R,r).

Let T(N)=∑^N_{R=3} ∑^{⌊(R−1)/2⌋}_{r=1} S(R,r) be the sum of S(R,r) for R and r positive integers, R≤N and 2r<R.

You are given:
C(3, 1) = {(3, 0), (-1, 2), (-1,0), (-1,-2)}
C(2500, 1000) = {(2500, 0), (772, 2376), (772, -2376), (516, 1792), (516, -1792), (500, 0), (68, 504), (68, -504),
                 (-1356, 1088), (-1356, -1088), (-1500, 1000), (-1500, -1000)}

Note: (-625, 0) is not an element of C(2500, 1000) because sin(t) is not a rational number for the corresponding values
of t.

S(3, 1) = (|3| + |0|) + (|-1| + |2|) + (|-1| + |0|) + (|-1| + |-2|) = 10

T(3) = 10; T(10) = 524; T(100) = 580442; T(10^3) = 583108600.

Find T(10^6).
"""

import sys
from math import pi, cos, acos, sin, ceil, gcd
from itertools import count
import numpy as np
from time import clock

def pimuls_and_x1(R, r, a, pythag_triples, max_powers):
  n = r // gcd(R, r) if R % r else 1
  
  nmod2 = n % 2
  nm1_divisible_4 = (n - 1) % 4 == 0
  
  n0 = 0
  
  if n == 1:
    n1 = 0
    n2 = 0
  elif n == 2:
    n1 = 0
    n2 = 2
  elif nm1_divisible_4:
    n1 = n + 1
    n2 = (3*n + 1) // 2
  else:
    n1 = 2*ceil(n/4)
    n2 = n + nmod2
  
  if n % 4 == 0:
    result = [(n0, a), (n1, a), (n2, a)]
  elif nmod2 == 0:
    result = [(n0, a), (n1, -a), (n2, a)]
  elif nm1_divisible_4:
    result = [(n0, a), (n1, -a), (n2, 0)]
  else:
    result = [(n0, a), (n1, 0), (n2, -a)]
  
  if n == 1:
    k = R // r - 1
    # can this be made more efficient???
    for pa, pb, pc in pythag_triples:
      if k > max_powers[pc]:
        break
      factor = k*pc**k
      if factor > a:
        break
      elif a % factor == 0:
        r1, r2 = pa*a//pc, pb*a//pc
        result = [*result, (0, r1), (0, -r1), (0, r2), (0, -r2)]
  elif n == 2 and R / r == 2.5 and a % 375 == 0:
    # experiment: can "R / r == 2.5" be removed?
    r1 = 7*a/25
    result = [*result, (0, r1), (2, r1), (0, -r1), (2, -r1)]
  
  return result

A = np.mat('1 -2 2; 2 -1 2; 2 -2 3')
B = np.mat('1 2 2; 2 1 2; 2 2 3')
C = np.mat('-1 2 2; -2 1 2; -2 2 3')

def pythagorean_triples_up_to(limit): # all Pythagorean triples with 2c^2 < limit
  stack = [np.mat('3; 4; 5')]
  triples = []
  
  while stack:
    current = stack.pop(0)
    triples.append(tuple(map(int, np.squeeze(np.asarray(current)))))
    
    children = [A*current, B*current, C*current]
    for child in children:
      if 2*int(child[-1])**2 < limit:
        stack.append(child)
  
  return triples

def highest_powers(pythag_triples, limit): # returns dict of {c: highest exponent n with 2c^n <= limit}
  result = {}
  for _, _, c in pythag_triples:
    exponent = next(i for i in count() if 2*c**(i+1) > limit)
    result[c] = exponent
  return result

def S(R, r, pythag_triples, max_powers):
  # x(t) = acos(t) + rcos(kt), y(t) = asin(t) - rsin(kt)
  a = R - r
  k = a / r
  
  # x1 = acos(t), x2 = rcos(kt), y1 = asin(t), y2 = rsin(kt)
  # iterate through values of x1, see which values of t make x2, y1, y2 integers
  
  total = 0
  
  for pimul, x1 in pimuls_and_x1(R, r, a, pythag_triples, max_powers):
    acos_ = acos(x1/a)
    
    t = pimul*pi - acos_
    kt = k*t
    
    x2 = r*cos(kt)
    y1 = a*sin(t)    
    y2 = r*sin(kt)
    
    x = round(x1 + x2)
    y = round(y1 - y2)
    
    if y == 0:
      total += abs(x)
    else:
      total += 2*abs(x) + 2*abs(y)
  
  return total

def T(N):
  pythag_triples = sorted(pythagorean_triples_up_to(N), key=lambda triple: triple[-1])
  print('Pythagorean triples generated; there are {} triples: {}'.format(len(pythag_triples), pythag_triples))
  
  max_powers = highest_powers(pythag_triples, N)
  
  timestamp = clock()
  timestamps = [timestamp]
  
  total = 0
  for R in range(3, N+1):
    r_total = 0
    
    for r in range(1, ceil(R/2)):
      this_s = S(R, r, pythag_triples, max_powers)
      total += this_s
      r_total += this_s
    
    if R % 100 == 0:
      new_timestamp = clock()
      timestamps.append(new_timestamp)
      
      coeffs = np.polyfit(timestamps, list(range(0, R+1, 100)), 1)
      projected = np.polyval(coeffs, N)
      projh, projmins = divmod(projected, 3600)
      projm, projs = divmod(projmins, 60)
      
      print('R={}, total={} ({} this time), took {:.4f} seconds (R={} projected to take {:.0f}h{:.0f}m{:.0f}s)'
        .format(R, total, r_total, new_timestamp - timestamp, N, projh, projm, projs))
      timestamp = new_timestamp
      
      sys.stdout.flush()
  
  return total

print(T(1000000))
