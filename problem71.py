#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 71:

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d ≤ 1,000,000 in ascending order of size, find the numerator of the
fraction immediately to the left of 3/7.
"""

# So, um, this *will* eventually find the answer. It'll just take several days until you decide to brute force the
# general area where the solutions are all coming from. There's a much better way to do this.
# This solution generates *all* coprime pairs less than 1000000 using the formula that if (m, n) is the pair with m>n,
# then starting with (2, 1), all coprime pairs can be generated recursively as (2m - n, m), (2m + n, m), and (m + 2n, n)
# It keeps track only of the one directly left of 3/7.
# It gets *close*, but takes days to get the correct answer.
# For the brute-force method, check problem71_observed.py

best_numer = -1
best_denom = 1

to_check = [(2, 1)]

while to_check:
  m, n = to_check.pop()
  if m % 100000 == 3:
    print(m, n, '|', best_numer, '/', best_denom, '|', len(to_check))
  
  # a/b < c/d <=> a*d < b*c
  if 7*n < 3*m and n*best_denom > m*best_numer:
    best_numer = n
    best_denom = m
  
  mb1 = 2*m - n
  if mb1 <= 1000000:
    to_check.append((mb1, m))
  
  mb2 = 2*m + n
  if mb2 <= 1000000:
    to_check.append((mb2, m))
  
  mb3 = m + 2*n
  if mb3 <= 1000000:
    to_check.append((mb3, n))

print(best_numer, '/', best_denom, sep='')
print(best_numer)
