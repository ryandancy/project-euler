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

def is_integer(x):
  return abs(round(x) - x) < 0.00000001

def pimuls(R, r):
  n = r // gcd(R, r) if R % r else 1
  
  if n == 1:
    return [0]
  elif n == 2:
    if R % 625 == 0 and r % 250 == 0:
      return [-2, 0, 2]
    else:
      return [-2, 0]
  
  if (n - 1) % 4 == 0:
    n0 = (-3*n - 1) // 2
    return [n0, -n - 1, 0, -n0]
  else:
    n1 = -2*ceil(n/4)
    return [-n - (n % 2), n1, 0, -n1]

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

def x1s(R, r, a, pythag_triples, max_powers):
  result = [-a, 0, a]
  
  k = R / r
  if k.is_integer():
    k = int(k) - 1
    # can this be made more efficient???
    for pa, pb, pc in pythag_triples:
      if k > max_powers[pc]:
        break
      factor = k*pc**k
      if factor > a:
        break
      elif a % factor == 0:
        r1, r2 = pa*a//pc, pb*a//pc
        result += [r1, -r1, r2, -r2]
  elif k == 2.5 and a % 375 == 0:
    # special case of lone 7/25
    r = 7*a//25
    result += [r, -r]
  
  return result

def S(R, r, pythag_triples, max_powers):
  # x(t) = acos(t) + rcos(kt), y(t) = asin(t) - rsin(kt)
  a = R - r
  k = a / r
  
  # x1 = acos(t), x2 = rcos(kt), y1 = asin(t), y2 = rsin(kt)
  # iterate through values of x1, see which values of t make x2, y1, y2 integers
  
  x1_to_check = x1s(R, r, a, pythag_triples, max_powers)
  
  lattice = set()
  
  pimuls_ = pimuls(R, r)#[b for c in range(0, 2*r+1, 2) for b in ([c] if c == 0 else [-c, c])]
  
  for x1 in x1_to_check:#[b for c in range(-a, a + 1) for b in ([c] if c == a else [c, c + 0.5])]:
    acos_ = acos(x1/a)
    
    for pimul in pimuls_:
      if pimul == 0:
        ts = (acos_, -acos_)
      else:
        pimuled = pimul*pi
        ts = (acos_ + pimuled if pimul < 0 else pimuled - acos_,)
      
      for t in ts:
        kt = k*t
        
        x2 = r*cos(kt)
        if not is_integer(x2):
          continue
        
        y1 = a*sin(t)
        if not is_integer(y1):
          continue
        
        y2 = r*sin(kt)
        if not is_integer(y2):
          continue
        
        x = round(x1 + x2)
        y = round(y1 - y2)
        
        lattice.add((x, y))
  
  return sum(abs(a) for xy in lattice for a in xy)

def T(N):
  pythag_triples = sorted(pythagorean_triples_up_to(N), key=lambda triple: triple[-1])
  print('Pythagorean triples generated; there are {} triples: {}'.format(len(pythag_triples), pythag_triples))
  
  max_powers = highest_powers(pythag_triples, N)
  
  timestamp = clock()
  
  total = 0
  for R in range(3, N+1):
    r_total = 0
    
    for r in range(1, ceil(R/2)):
      this_s = S(R, r, pythag_triples, max_powers)
      total += this_s
      r_total += this_s
    
    if R % 100 == 0:
      new_timestamp = clock()
      print('R={}, total={} ({} this time), took {:.4f} seconds'.format(R, total, r_total, new_timestamp - timestamp))
      timestamp = new_timestamp
      
      sys.stdout.flush()
  return total

print(T(1000000))
