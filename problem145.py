#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 145:

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits.
For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are
reversible. Leading zeroes are not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?
"""

# Largely brute-force: check if each n is reversible from n=1 to n=10^9/2, add 2 for each one
# If n is reversible, reverse(n) is added to a "don't visit" set which each n is check against before proceeding
# n goes only up to 10^9/2 (not 10^9) because any 10^9/2 < n < 10^9 will have a counterpart 0 < reverse(n) < 10^9/2
#   and n would already have been found as the reverse of reverse(n)

def reverse(n):
  return int(str(n)[::-1])

ODD_DIGITS = {'1', '3', '5', '7', '9'}
def check_reversible(n):
  if n % 10 == 0:
    return False
  rev = reverse(n)
  return rev if set(str(n + rev)) <= ODD_DIGITS else False

num_reversible = 0
dont_visit = set()

for n in range(1, 10**9//2):
  if n in dont_visit:
    dont_visit.remove(n)
    continue
  
  rev = check_reversible(n)
  if rev:
    num_reversible += 2
    dont_visit.add(rev)

print(num_reversible)
