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

from math import pi, cos, acos, sin, ceil
from fractions import Fraction

def is_integer(x):
  return abs(round(x) - x) < 0.0001

def S(R, r):
  # x(t) = acos(t) + rcos(kt), y(t) = asin(t) - rsin(kt)
  a = R - r
  k = a / r
  
  # x1 = acos(t), x2 = rcos(kt), y1 = asin(t), y2 = rsin(kt)
  # iterate through values of x1, see which values of t make x2, y1, y2 integers
  
  x1_to_check = [
    -2, -1, 0, 1, 2,
    -a, a,
    -24*a/25, 24*a/25,
    -4*a/5, 4*a/5,
    -3*a/5, 3*a/5,
    -7*a/25, 7*a/25,
    -28*a/53, 28*a/53, # last might not be necessary
    -45*a/53, 45*a/53,
  ]
  
  lattice = set()
  
  for x1 in x1_to_check:#range(-a, a + 1):
    if not is_integer(x1):
      continue
    
    acos_ = acos(x1/a)
    for pimul in range(0, 100, 2):
      for t in {acos_ - pimul*pi, pimul*pi - acos_}:
        x2 = r*cos(k*t)
        if not is_integer(x2):
          continue
        
        y1 = a*sin(t)
        if not is_integer(y1):
          continue
        
        y2 = r*sin(k*t)
        if not is_integer(y2):
          continue
        
        x = round(x1 + x2)
        y = round(y1 - y2)
        
        if x1 not in x1_to_check:
          print('{} not in ({}, {})!! ({}, {})'.format(x1, R, r, x, y))
        
        lattice.add((x, y))
  
  return sum(abs(a) for xy in lattice for a in xy)

def T(N):
  total = 0
  for R in range(3, N+1):
    for r in range(1, ceil(R/2)):
      total += S(R, r)
      #print(R, r, total)
  return total

# This overshoots by 240. How??
print(T(100))

# for numer in range(3, 11):
#   for denom in range(1, ceil(numer/2)):
#     r = 100000*denom
#     R = numer*r//denom
#     a = R - r
    
#     result = naive_c(R, r)
    
#     x1s = [res[3] for res in result]
#     x2s = [res[4] for res in result]
#     y1s = [res[5] for res in result]
#     y2s = [res[6] for res in result]
    
#     print('x1 for ({}, {}, a={}): {} = {}*a'.format(R, r, a, x1s, [str(Fraction(x1, a)) for x1 in x1s]))
#     print('x2 for ({}, {}, a={}): {} = {}*r'.format(R, r, a, x2s, [str(Fraction(x2, r)) for x2 in x2s]))
#     print('y1 for ({}, {}, a={}): {} = {}*a'.format(R, r, a, y1s, [str(Fraction(y1, a)) for y1 in y1s]))
#     print('y2 for ({}, {}, a={}): {} = {}*r'.format(R, r, a, y2s, [str(Fraction(y2, r)) for y2 in y2s]))
#     print('----------------------------------------------------------')
