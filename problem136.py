#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 136:

The positive integers, x, y, and z, are consecutive terms of an arithmetic progression. Given that n is a positive
integer, the equation, x^2 − y^2 − z^2 = n, has exactly one solution when n = 20:

13^2 − 10^2 − 7^2 = 20

In fact there are twenty-five values of n below one hundred for which the equation has a unique solution.

How many values of n less than fifty million have exactly one solution?
"""

'''
Since x, y, and z form an arithmetic sequence, x - y = y - z. Thus x + z = 2y and y = (x + z)/2. Substituting this into
the general equation, we get:

x^2 - ((x + z)/2)^2 - z^2 = n
x^z - (x^2 + 2xz + z^2)/4 - z^2 = n
4x^2 - x^2 - 2xz - z^2 - 4z^2 = 4n
3x^2 - 2xz - 5z^2 - 4n = 0

To better conform to mathematical standards, let us rename z to y; this has no distinction on the middle y term of the
arithmetic sequence from earlier. Thus 3x^2 - 2xy - 5y^2 - 4n = 0.

A solution exists for a given n when this hyperbola has a positive integral point. According to [1], a hyperbola of the
form ax^2 + bxy + cy^2 + dx + ey + J = 0, where k^2 = b^2 - 4ac with k being an integer may have its integral points
found easily; this specific hyperbola, with a = 3, b = -2, c = -5, d = e = 0, and J = -4n, qualifies as such with
k = sqrt((-2)^2 - 4(3)(-5)) = 8.

An integer I is defined by [1] such that I = k^2(d^2 - 4aJ) - (2ae - bd)^2; in our case, I = 8^2(-4(3)(-4n)) = 3072n.
When simplified and variables equal to zero are removed, [1] tells us that

x_i = (d_i(b + k) - I/d_i(b - k))/(4ak^2)
y_i = (I/d_i - d_i)/(2k^2)

where d_i is the ith divisor of I. When our values are substituted and the equations simplified, the formulae reduce to

x_i = d_i/128 + 40n/d_i
y_i = 24n/d_i - d_i/128

When both x_i and y_i are positive integers for a given n and d_i, there is a solution for the original equation.

This program loops through each n and each divisor of I = 3072n, keeping track of whether it has found a solution. If
it finds more than one, it continues to the next n without generating the rest of the divisors; if it goes through all
divisors and finds exactly one solution, 1 is added to the running count.

This program uses sympy.ntheory.divisors in order to speed up the process of finding divisors of massive numbers. It
runs in ~2 hours 45 minutes.

[1]: Zelator, K. (2009). Integral points on hyperbolas over z: A special case. Providence: Department of Mathematics
        and Computer Science, Rhode Island College. Retrieved from https://arxiv.org/ftp/arxiv/papers/0907/0907.3675.pdf
'''

from sympy.ntheory import divisors

num_one_solution = 0

for n in range(1, 50000000):
  no_solutions = True
  n40 = 40*n
  n24 = 24*n
  for di in divisors(3072*n, generator=True):
    div_128 = di/128
    x = div_128 + n40/di
    
    if not x.is_integer():
      continue
    
    y = n24/di - div_128
    
    if y > 0 and y.is_integer():
      if no_solutions:
        no_solutions = False
      else:
        # multiple solutions
        break
  else:
    if not no_solutions:
      num_one_solution += 1

print(num_one_solution)
