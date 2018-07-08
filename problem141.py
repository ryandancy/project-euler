#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 141:

A positive integer, n, is divided by d and the quotient and remainder are q and r respectively. In addition d, q, and r
are consecutive positive integer terms in a geometric sequence, but not necessarily in that order.

For example, 58 divided by 6 has quotient 9 and remainder 4. It can also be seen that 4, 6, 9 are consecutive terms in a
geometric sequence (common ratio 3/2). We will call such numbers, n, progressive.

Some progressive numbers, such as 9 and 10404 = 102^2, happen to also be perfect squares.
The sum of all progressive perfect squares below one hundred thousand is 124657.

Find the sum of all progressive perfect squares below one trillion (10^12).
"""

'''
If x, y, and z are integer elements of a geometric sequence (in order), then x/y = y/z -> y^2 = xz. As well, given the
definitions in the question, n = qd + r. Since any of q, d, and r may be any term in the geometric sequence, there are
three distinct possibilities:

q = x, d = y, r = z / q = y, d = x, r = z
q = y, d = z, r = x / q = z, d = y, r = x
q = z, d = x, r = y / q = x, d = z, r = y

Note that since multiplication is commutative, the values of q and d may always be swapped and the result will be the
same; thus there are only these three distinct possibilities.

We now rearrange each possibility to relate d to r:

If q = x, d = y, and r = z, then:
d^2 = qr
q = d^2/r
qd + r = n
n = d(d^2/r) + r
nr = d^3 + r^2
d = cbrt(r(n - r))

If q = y, d = z, and r = x, then:
q^2 = dr
q = sqrt(dr)
qd + r = n
d*sqrt(dr) + r = n
d^3*r = (n - r)^2
d = cbrt((n - r)^2/r)

However, note that iff n/d = q with remainder r, then n/q = d with remainder r, since both give the equation n = qd + r.
Thus q and d are entirely equivalent; the two equations above will give different results (the smaller and larger of the
equivalent q and d), but both will have an integer solution if n in a progressive number.

If q = z, d = x, and r = y, then:
r^2 = qd
qd + r = n
r^2 + r = n
However, note that n is a perfect square; thus r^2 + r = k^2 for some positive integer k. Then:
r = k^2 - r^2 = (k + r)(k - r)
However, the differences between squares (3, 5, 7, 9, ...) have a slope of 2, while the positive integers naturally have
a slope of 1; thus the differences between squares outpace the square root of the lower square of the difference (r^2),
and thus I submit that this equation has no positive integer solution and thus r != y.

We now have two equations, either of which may be used to test for progressive numbers: d = cbrt(r(n - r)) and d =
cbrt((n - r)^2/r). The former is simpler, so I have chosen to use it. Note that 0 < r < d < n; it has been observed
(though not proven) that d < sqrt(n).

Consider the first equation, d = cbrt(r(n - r)). There are two multiplicands here: r and n - r. For simplicity, let us
define that a = r, b = n - r, and k = sqrt(n), all of which are integers. The problem then becomes the following: for
0 < a < b < k < sqrt(10^12) = 10^6, a + b = k^2, what is the sum of all values of k^2 for which ab is a perfect cube?

This problem is solved through iterating through the perfect cubes (where the cube root, d, is less than 10^6) and
checking their divisors. All non-equal divisor pairs ((a, cube / a) for a < sqrt(cube)) are checked; if a + b is square
and less than 10^12 and a is less than the cube root (d), the solution is checked to make sure a + b actually fits the
constraints of a progressive perfect square (as three non-solutions were being marked as solutions), and if so, a + b
is added to a running sum.

sympy.ntheory.divisors is used to generate the divisors of each cube as it is much faster than a homegrown algorithm.
This program outputs the correct answer in approximately 10 minutes.
'''

from math import sqrt
from sympy.ntheory import divisors

sum_ = 0
found = 0

for d in range(1, 10**6):
  cube = d ** 3
  sqrt_cube = sqrt(cube)
  
  for a in divisors(cube):
    if a >= sqrt_cube:
      break
    
    b, remainder = divmod(cube, a)
    if remainder == 0:
      n = a + b
      
      if n > 10**12:
        continue
      
      sqrt_n = sqrt(n)
      if sqrt_n.is_integer() and a < d and n % d == a: # the last part is to make sure this is actually a solution
        sum_ += n
        found += 1

print(sum_)
