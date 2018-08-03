#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 74:

The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:

1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169; it turns out
that there are only three such loops that exist:

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting
number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?
"""

# Fairly simple semi-brute-force recursive method
# Keeps a list of known chain lengths, recurses until one of those is reached
# Runs in ~5 seconds

from math import factorial

not_checked = set(range(1, 1000000))
chain_lengths = {169: 3, 363601: 3, 1454: 3, 871: 2, 45361: 2, 872: 2, 45362: 2}

def check_chain(n, count=1):
  nxt = sum(map(factorial, map(int, str(n))))
  if nxt == n:
    return count
  elif nxt in chain_lengths:
    return chain_lengths[nxt] + count
  else:
    return check_chain(nxt, count + 1)

while not_checked:
  n = not_checked.pop()
  chain_lengths[n] = check_chain(n)

print(sum(map(lambda x: x[0] < 1000000 and x[1] == 60, chain_lengths.items())))
