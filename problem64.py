#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 64:

All square roots are periodic when written as continued fractions and can be written in the form:

√N = a_0 + 1/(a_1 + 1/(a_2 + 1/(a_3 + ...)))

For example, let us consider √23:

√23 = 4 + √23 - 4 = 4 + 1/(1/(√23 - 4)) = 4 + 1/(1 + (√23 - 3)/7)

If we continue we would get the following expansion:

√23 = 4 + 1/(1 + 1/(3 + 1/(1 + 1/(8 + ...))))

The process can be summarised as follows:

a_0 = 4, 1/(√23 - 4) = (√23 + 4)/7 = 1 + (√23 - 3)/7
a_1 = 1, 7/(√23 - 3) = 7(√23 + 3)/14 = 3 + (√23 - 3)/2
a_2 = 3, 2/(√23 - 3) = 2(√23 + 3)/14 = 1 + (√23 - 4)/7
a_3 = 1, 7/(√23 - 4) = 7(√23 + 4)/7 = 8 + √23 - 4
a_4 = 8, 1/(√23 - 4) = 7(√23 + 3)/14 = 3 + (√23 - 3)/7

It can be seen that the sequence is repeating. For conciseness, we use the notation √23 = [4;(1,3,1,8)], to indicate
that the block (1,3,1,8) repeats indefinitely.

The first ten continued fraction representations of (irrational) square roots are:

√2=[1;(2)], period=1
√3=[1;(1,2)], period=2
√5=[2;(4)], period=1
√6=[2;(2,4)], period=2
√7=[2;(1,1,1,4)], period=4
√8=[2;(1,4)], period=2
√10=[3;(6)], period=1
√11=[3;(3,6)], period=2
√12= [3;(2,6)], period=2
√13=[3;(1,1,1,1,6)], period=5

Exactly four continued fractions, for N ≤ 13, have an odd period.

How many continued fractions for N ≤ 10000 have an odd period?
"""

# It turns out that the first repeating term of the continued fraction for √N is 2N
# Using this (plus some integer trickery to avoid floating point errors), the solution is found in ~0.25 seconds

from math import floor, sqrt

def sqrt_period_length(n):
  # https://stackoverflow.com/a/12188588 to avoid floating point errors
  # I don't entirely understand it but it works
  
  sqrt_n = sqrt(n)
  r = floor(sqrt_n)
  
  if r == sqrt(n):
    # n is square
    return 0
  
  result = 0
  
  a = r
  p = 0
  q = 1
  
  while True:
    p = a*q - p
    q = (n - p*p) // q
    a = (r + p) // q
    result += 1
    if a == 2*r:
      return result

print(sum(map(lambda n: sqrt_period_length(n) % 2 == 1, range(2, 10001))))
