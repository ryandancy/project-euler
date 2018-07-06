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

from math import sqrt
import sys

#def is_perfect_cube(n):
#  return int(round(n**(1/3)))**3 == n

sum_ = 9 # the only one with r=1
num_found = 0

for k in range(1, 1000000):
  if k % 100 == 0:
    sys.stderr.write('\rFound: {} | Sum: {} | Checked: k={} ({:.2f}%)'.format(num_found, sum_, k, k / 10000))
    sys.stderr.flush()
  
  n = k**2
  n_squared = n**2
  
  # for r in range(1, k):
  #   n_minus_r = n - r
  #   d3_1 = r * n_minus_r
  #   if is_perfect_cube(d3_1):
  #     #print('d3_1', r, round(d3_1 ** (1/3)), n)
  #     sum_ += n
  #     num_found += 1
  #     break
    #d3_2 = n_minus_r**2 / r
    #if is_perfect_cube(d3_2):
      #print('d3_2', r, round(d3_2 ** (1/3)), n)
      #break
  #else:
    #continue
  
  #found = False
  
  # for d in range(1, k):
  #   d_cubed = d**3
  #   r = n + (d_cubed + sqrt(d_cubed * (4*n + d_cubed))) / 2
  #   if r.is_integer():
  #     print(int(r), d, n)
  #     found = True
  #     break
  
  # if not found:
  # found = False
  
  try:
    for d in range(int((n - 1) ** (1/3)), k):
      r2 = n - sqrt(n_squared - 4*d**3)
      if r2 % 2 == 0 and r2 > 2:
        #found = True
        print(int(r2/2), d, n)
        sum_ += n
        num_found += 1
        break
  except ValueError:
    # Math domain error: didn't find one in time, continue
    pass
  
  # if found:
  #   continue
  
  # for d in range(1, k):
  #   d_cubed = d**3
  #   r = n + (d_cubed + sqrt(d_cubed*(4*n + d_cubed))) / 2
  #   if r.is_integer() and r < d:
  #     print('b', r, d, n)
  #     sum_ += n
  #     num_found += 1
  #     break
  
  #if found:

print()
print(sum_)
sys.stderr.write('\n{}\n'.format(sum_))
