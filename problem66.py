#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 66:

Consider quadratic Diophantine equations of the form:

x^2 – Dy^2 = 1

For example, when D=13, the minimal solution in x is 6492 – 13×1802 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

32 – 2×22 = 1
22 – 3×12 = 1
92 – 5×42 = 1
52 – 6×22 = 1
82 – 7×32 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.
"""

'''
x^2 - Dy^2 = 1 is Pell's equation. The simplest solution (called the fundamental solution) for an arbitrary non-square D
is the first x and y satisfying the equation where x and y are the numerator and denominator respectively in a
convergent in the continued fraction of sqrt(D). (The terms of this continued fraction are a_0, a_1, ..., a_n such that
sqrt(D) = a_0 + 1/(a_1 + 1/(a_2 + 1/(a_3 + 1/(...)))); the convergents are then [a_0, a_0 + 1/a_1, a_0 + 1/(a_1 +
1/(a_2)), ...].)

This program calculates the convergents for each sqrt(D) for 1 <= D <= 1000 where D is not a perfect square, and
checks each numerator (x) and denominator (y) pair for whether they fit Pell's equation for the specific D. It runs in
less than 0.1 seconds.
'''

from math import sqrt, floor

def gen_continued_fraction_terms(n, sqrt_n): # assuming irrational
  # https://stackoverflow.com/a/12188588 to avoid floating point errors
  # I don't entirely understand it but it works
  
  r = floor(sqrt_n)
  yield r
  
  a = r
  p = 0
  q = 1
  
  while True:
    p = a*q - p
    q = (n - p*p) // q
    a = (r + p) // q
    yield int(a)

def gen_convergents(n, sqrt_n):
  numer = 1
  prev_numer = 0
  
  denom = 0
  prev_denom = 1
  
  for a in gen_continued_fraction_terms(n, sqrt_n):
    new_numer = a*numer + prev_numer
    new_denom = a*denom + prev_denom
    yield new_numer, new_denom
    
    prev_numer = numer
    numer = new_numer
    
    prev_denom = denom
    denom = new_denom

def minimal_x(d):
  sqrt_d = sqrt(d)
  if sqrt_d.is_integer():
    # Squares have no solutions
    return -1
  
  for x, y in gen_convergents(d, sqrt_d):
    if x*x - d*y*y == 1:
      return x

if __name__ == '__main__':
  print(max(range(1, 1001), key=minimal_x))
