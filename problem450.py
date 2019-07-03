#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import floor, log2, sqrt, gcd
from fractions import Fraction
from itertools import count
import numpy as np

"""
Project Euler Problem 450:

A hypocycloid is the curve drawn by a point on a small circle rolling inside a large circle. The
parametric equations of a hypocycloid centred at the origin and starting at the rightmost point is
given by:

x(t) = (R - r)cos(t) + r cos((R - r)/r t)
y(t) = (R - r)sin(t) - r sin((R - r)/r t)

Where R is the radius of the large circle and r the radius of the small circle.

Let C(R, r) be the set of distinct points with integer coordinates on the hypocycloid with radius
R and r and for which there is a corresponding value of t such that sin(t) and cos(t) are rational
numbers.

Let S(R, r) = sum_{(x, y) in C(R, r)} |x| + |y| be the sum of the absolute values of the x and y
coordinates of the points in C(R, r).

Let T(N) = sum_{R=3}^N sum_{r=1}^{floor((R-1)/2)} S(R, r) be the sum of S(R, r) for R and r positive
integers, R <= N and 2r < R.

You are given:
C(3, 1) = {(3, 0), (-1, 2), (-1, 0), (-1, -2)}
C(2500, 1000) = {(2500, 0), (772, 2376), (772, -2376), (516, 1792), (516, -1792), (500, 0), (68, 504),
  (68, -504), (-1356, 1088), (-1356, -1088), (-1500, 1000), (-1500, -1000)}

Note: (-625, 0) is not an element of C(2500, 1000) because sin(t) is not a rational number for the
corresponding values of t.

S(3, 1) = (|3| + |0|) + (|-1| + |2|) + (|-1| + |0|) + (|-1| + |-2|) = 10.

T(3) = 10; T(10) = 524; T(100) = 580442; T(10^3) = 583108600.

Find T(10^6).
"""

def normals(N): # sum of the normal points (t = npi/2 for integer n); O(log2(N))
  a = (N-1)//2
  odd = a * (a + 1) * (7*a + 8)
  even = 0
  for k in range(1, floor(log2(N))+1):
    m = (N+2**k)//(2**(k+1))
    even += 2**k * m * (m*m*(2**(k+3)-3) - 2**(k+1) - 9*m)
  return (odd + even) // 3

# Matrices for generating Pythagorean triples
A = np.mat('1 -2 2; 2 -1 2; 2 -2 3')
B = np.mat('1 2 2; 2 1 2; 2 2 3')
C = np.mat('-1 2 2; -2 1 2; -2 2 3')

def generate_pythagorean_triples(N):
  # Returns a, b, c where a**2 + b**2 = c**2, b is even and a is odd
  # Will return if: 3c^2 <= N --> c <= sqrt(N/3)
  # (i.e. there is at least one R <= N including the triple as a special)
  # Generates triples via https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples
  
  c_bound = sqrt(N/3)
  triples = [np.mat('3; 4; 5')]
  while triples:
    triple = triples.pop(0)
    a, b, c = triple.reshape(-1).tolist()[0]
    
    if c <= c_bound:
      yield a, b, c
      triples.append(A * triple)
      triples.append(B * triple)
      triples.append(C * triple)

def chebyshev_cos(n, cosx, sign=1, pifrac=Fraction(0)):
  # Computes cos(sign*arccos(cosx) + pifrac*pi) using the Chebyshev method:
  # cos(nx) = 2*cos(x)*cos((n-1)x) - cos((n-2)x)
  if n == 1:
    num, den = pifrac.numerator, pifrac.denominator
    if den == 1:
      if num % 2 == 0:
        # cos x
        return cosx
      else: # num % 2 == 1
        # cos(x+pi) = -cos x
        return -cosx
    elif den == 2:
      b, c = cosx.numerator, cosx.denominator
      a = round(sqrt(c*c - b*b))
      if num % 4 == 1:
        # cos(x+pi/2) = -sin x
        return Fraction(-a * sign, c)
      else: # num % 4 == 3 (others blocked by Fraction)
        # cos(x+3pi/2) = sin x
        return Fraction(a * sign, c)
    else:
      # cos will only be rational when pifrac is a half-integer or integer
      raise Exception(f'Unfamiliar pifrac: {pifrac}')
  elif n == 2:
    # double-angle identity: cos(2x) = 2(cos(x))^2 - 1
    return 2*chebyshev_cos(1, cosx, sign=sign, pifrac=pifrac)**2 - 1
  else:
    # aforementioned Chebyshev identity: cos(nx) = 2*cos(x)*cos((n-1)x) - cos((n-2)x)
    return (2 * chebyshev_cos(1, cosx, sign=sign, pifrac=pifrac)
      * chebyshev_cos(n - 1, cosx, sign=sign, pifrac=pifrac)
      - chebyshev_cos(n - 2, cosx, sign=sign, pifrac=pifrac))

def chebyshev_sin(n, cosx, sign=1, pifrac=Fraction(0)):
  # Computes sin(sign*arccos(cosx) + pifrac*pi) using the Chebyshev method:
  # sin(nx) = 2*cos(x)*sin((n-1)x) - sin((n-2)x)
  if n == 1:
    num, den = pifrac.numerator, pifrac.denominator
    if den == 1:
      b, c = cosx.numerator, cosx.denominator
      a = round(sqrt(c*c - b*b))
      if num % 2 == 0:
        # sin x
        return Fraction(a * sign, c)
      else: # num % 2 == 1
        # sin(x+pi) = -sin x
        return Fraction(-a * sign, c)
    elif den == 2:
      if num % 4 == 1:
        # sin(x+pi/2) = cos x
        return cosx
      else: # num % 4 == 3 (others blocked by Fraction)
        # sin(x+3pi/2) = -cos x
        return -cosx
    else:
      # sin will only be rational when pifrac is a half-integer or integer
      raise Exception(f'Unfamiliar pifrac: {pifrac}')
  elif n == 2:
    # double-angle identity: sin(2x) = 2sin(x)cos(x)
    return (2 * chebyshev_sin(1, cosx, sign=sign, pifrac=pifrac)
      * chebyshev_cos(1, cosx, sign=sign, pifrac=pifrac))
  else:
    # aforementioned Chebyshev identity: sin(nx) = 2*cos(x)*sin((n-1)x) - sin((n-2)x)
    return (2 * chebyshev_cos(1, cosx, sign=sign, pifrac=pifrac)
      * chebyshev_sin(n - 1, cosx, sign=sign, pifrac=pifrac)
      - chebyshev_sin(n - 2, cosx, sign=sign, pifrac=pifrac))

def pattern(Q, af, bf):
  # Produces a dictionary of all possible combinations of af and bf (i.e. negative, in reverse order)
  # to the produced sinQt, cosQt with t = arcsin of the first one and arccos of the second one
  # (I think). This is done using multiples of pi: x, pi - x, pi + x, 2pi - x.
  # It's a dictionary for ease of looking up values for use with fractional Q.
  
  patt = {}
  
  m = 2 if Q % 2 == 0 else 3
  
  for cosx, sign, pifrac in [
    (af, 1, Fraction(0)), (af, -1, Fraction(m, 2)),
      (af, 1, Fraction(m, 2)), (af, -1, Fraction(m)),
    (bf, 1, Fraction(0)), (bf, -1, Fraction(m, 2)),
      (bf, 1, Fraction(m, 2)), (bf, -1, Fraction(m)),
  ]:
    sinQt = chebyshev_sin(Q, cosx, sign=sign, pifrac=pifrac)
    cosQt = chebyshev_cos(Q, cosx, sign=sign, pifrac=pifrac)
    sint = chebyshev_sin(1, cosx, sign=sign, pifrac=pifrac)
    cost = chebyshev_cos(1, cosx, sign=sign, pifrac=pifrac)
    
    patt[sint, cost] = (sinQt, cosQt)
  
  return patt

def specials(N):
  special_total = 0
  
  for a, b, c in generate_pythagorean_triples(N):
    for Q in count(2):
      if (Q + 1) * c**Q > N:
        # No possible values of R <= N
        break
      
      af = Fraction(a, c)
      bf = Fraction(b, c)
      
      # first, forwards - always
      # calculate the sum of all r-values such that R <= N
      r_bound = N // ((Q + 1) * c**Q)
      sum_r = c**Q * r_bound * (r_bound + 1) // 2
      
      patt = pattern(Q, af, bf)
      
      for (sint, cost), (sinQt, cosQt) in patt.items():
        # add the sums of all the points with this Q and triple
        special_total += sum_r * (abs(Q*cost + cosQt) + abs(Q*sint - sinQt))
      
      # then, backwards
      for Qn in count(Q + 1):
        if gcd(Qn, Q) != 1: # reduces to something simpler - ignore
          continue
        
        Qf = Fraction(Qn, Q)
        if (Qf + 1) * c**Qn > N: # equivalent to (Qf + 1) * (c**Q)**Qf
          break
        
        # this method of calculating r_bound isn't *strictly* necessary for N=10^6,
        # but for N>10^6 we have to consider the case where c and Q aren't multiples
        # but also aren't coprime
        g = gcd(c, Q)
        r_bound = (N * g) // (c**Qn * (Qn + Q))
        if r_bound == 0:
          # no r-values: don't bother calculating any further
          break
        sum_r = (Q // g) * c**Qn * r_bound * (r_bound + 1) // 2
        
        npatt = pattern(Qn, af, bf)
        
        for (sintQ, costQ), (sint, cost) in patt.items():
          # sin(Qn/Q t) = sin(Qn sin arcsin(1/Q t)); 1/Q's patterns are just the reverse
          sinQt, cosQt = npatt[sintQ, costQ]
          special_total += sum_r * (abs(Qf*cost + cosQt) + abs(Qf*sint - sinQt))
  
  return special_total

def T(N):
  return normals(N) + specials(N)

if __name__ == '__main__':
  print(T(10**6))
