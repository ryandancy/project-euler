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

# THIS SHOULD WORK

from math import acos, cos, sin, pi, sqrt
from sympy.ntheory import factorint
import numpy as np
print('Sympy and Numpy loaded')

def phi(R, factors):
  prod = R
  for p in factors:
    prod *= 1 - 1/p
  return round(prod)

def psi(factors):
  prod = 1
  for p in factors:
    prod *= 1 - p
  return prod

def triangle(n):
  return n*(n+1)//2

A = np.mat('1 -2 2; 2 -1 2; 2 -2 3')
B = np.mat('1 2 2; 2 1 2; 2 2 3')
C = np.mat('-1 2 2; -2 1 2; -2 2 3')

def pythagorean_triples_up_to(limit): # all Pythagorean triples with 2c^2<=limit, lone squares with 5sqrt(c)^3<=limit
  stack = [np.mat('3; 4; 5')]
  triples = []
  lone_squares = []
  squares_searching_for = set()
  
  while stack:
    current = stack.pop(0)
    
    c = int(current[-1])
    if c in squares_searching_for:
      lone_squares.append(sorted(tuple(map(int, np.squeeze(np.asarray(current))))))
      squares_searching_for.remove(c)
    
    ltlimit = 2*c**2 <= limit
    
    #print(squares_searching_for)
    
    if ltlimit:
      triples.append(tuple(map(int, np.squeeze(np.asarray(current)))))
      if 5*c**3 <= limit:
        squares_searching_for.add(c**2)
    
    if ltlimit or squares_searching_for:
      children = [A*current, B*current, C*current]
      for child in children:
        if ((squares_searching_for and any(int(child[-1]) <= c for c in squares_searching_for))
              or 2*int(child[-1])**2 <= limit):
          stack.append(child)
  
  return triples, lone_squares

def eval_special(R, r, x1s_and_pimuls): # pimul always 0
  a = R - r
  k = a / r
  
  total = 0
  
  for x1, pimul in x1s_and_pimuls:
    acos_ = acos(x1/a)
    t = pimul*pi - acos_
    kt = k*t
    
    x2 = r*cos(kt)
    y1 = a*sin(t)
    y2 = r*sin(kt)
    
    x = round(x1) + round(x2)
    y = round(y1) - round(y2)
    
    #print(R, r, x1, x, y)
    
    total += 2*abs(x) + 2*abs(y)
  
  return total

def T(N):
  base = 0
  for R in range(3, N+1):
    factors = factorint(R)
    n = N // R
    
    phir = phi(R, factors)
    
    t = 2*R*phir
    
    if R % 4 != 0:
      residue = R % 4
      if residue == 3:
        residue = 1
      
      sum_coprimes = (R*phir - residue*psi(factors)) // 8
      
      if R % 2 == 0:
        t -= 4*sum_coprimes
      else:
        t -= 2*sum_coprimes
    
    #print(R, triangle(n) * t)
    
    base += triangle(n) * t
  
  print('Base found')
  
  special = 0
  
  triples, lone_squares = pythagorean_triples_up_to(N)
  
  for (pa, pb, pc) in triples:
    degree = 2
    
    base_r = pc**degree
    base_R = (degree+1)*base_r
    
    while base_R <= N:
      mul = 1
      
      this = 0
      
      while True:
        R = base_R*mul
        r = base_r*mul
        a = R - r
        
        if R > N:
          break
        
        x1s_and_pimuls = [(pa*a//pc, 0), (-pa*a//pc, 0), (pb*a//pc, 0), (-pb*a//pc, 0)]
        special += eval_special(R, r, x1s_and_pimuls)
        this += eval_special(R, r, x1s_and_pimuls)
        
        #print(R, r, this)
        mul += 1
      
      #print((pa, pb, pc), degree, this)
      
      degree += 1
      base_r = pc**degree
      base_R = (degree+1)*base_r
  
  # lone squares
  for pa, pb, pc in lone_squares:
    sqrtc = sqrt(pc)
    cube = sqrtc**3
    base_r = r = 2*cube
    base_R = R = 5*cube
    
    this = 0
    
    mul = 1
    while R <= N:
      a = R - r
      pos = pa*a//pc
      
      # this works but in a roundabout fashion
      x1s_and_pimuls = [(pos, 0), (pos, 1), (pos, 2), (pos, 3)]
      special += eval_special(R, r, x1s_and_pimuls)
      this += eval_special(R, r, x1s_and_pimuls)
      
      #print(R, r, this)
      
      mul += 1
      R = base_R*mul
      r = base_r*mul
    
    #print('lone square:', (pa, pb, pc), this)
  
  # base_R = R = 625
  # base_r = r = 250
  # mul = 1
  # this = 0
  # while R <= N:
  #   a = R - r
  #   x1s_and_pimuls = [(7*a//25, 0), (7*a//25, 2), (-7*a//25, 0), (-7*a//25, 2)]
  #   special += eval_special(R, r, x1s_and_pimuls)
  #   this += eval_special(R, r, x1s_and_pimuls)
  #   mul += 1
  #   R = base_R*mul
  #   r = base_r*mul
  # print('lone 7/25', this)
  
  print('Specials evaluated')
  
  # for (c, degree), add in special_lookup.items():
  #   min_R = (degree+1)*c**degree
    
  #   mul = 1
  #   R = min_R
    
  #   #this_total = 0
    
  #   while R <= N:
  #     special += mul*add
  #   #  this_total += mul*add
  #   #  print('Applied c={}, degree={} at R={}'.format(c, degree, R))
  #     mul += 1
  #     R = mul*min_R
    
  #   #if this_total:
  #   #  print('c={}, degree={}: {}'.format(c, degree, this_total))
  
  # # lone 7/25
  # min_R = 625
  # add = 4236
  
  # #this_total = 0
  
  # mul = 1
  # R = min_R
  # while R <= N:
  #   special += mul*add
  #   #this_total += mul*add
  #   mul += 1
  #   R = mul*min_R
  
  #print('Lone 7/25:', this_total)
  
  #print(base, special)
  return base + special

print(T(1000000))

# from math import gcd, ceil
# for R in range(3, 51):
#   sc1 = sum(r for r in range(1, ceil(R/2)) if gcd(R, r) == 1)
  
#   d = R % 4
#   if d == 3:
#     d = 1
  
#   sc2 = (R * phi(R) - d * psi(R)) // 8
  
#   print(R, sc1, sc2)
