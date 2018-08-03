#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 78:

Let p(n) represent the number of different ways in which n coins can be separated into piles. For example, five coins
can be separated into piles in exactly seven different ways, so p(5)=7.

OOOOO
OOOO   O
OOO   OO
OOO   O   O
OO   OO   O
OO   O   O   O
O   O   O   O   O

Find the least value of n for which p(n) is divisible by one million.
"""

# Uses the pentagonal number theorem to calculate each successive p(n) until 10^6|p(n)
# Runs in ~15 seconds

from itertools import count

pmemoized = {}
def pentagonal(n):
  if n not in pmemoized:
    pmemoized[n] = (3*n*n - n) // 2
  return pmemoized[n]

memoized = {}
def p(n):
  if n < 0:
    return 0
  elif n == 0:
    return 1
  elif n not in memoized:
    result = 0
    
    for k in (a for ab in zip(count(1), count(-1, -1)) for a in ab):
      g = pentagonal(k)
      if n < g:
        break
      result += (-1 if k % 2 == 0 else 1) * p(n - g)
    
    memoized[n] = result
  
  return memoized[n]

print(next(n for n in count(1) if p(n) % 1000000 == 0))
