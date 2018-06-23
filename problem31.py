#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 31:

In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).

It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?
"""

# Start from 200p and go backwards, generating each possible combination that adds to 200

# Takes ~4 hours to run because combinations() is O(2^n)
# The time it takes to calculate the coins for each successive total grows exponentially

from collections import Counter
import sys

coins = [1, 2, 5, 10, 20, 50, 100, 200]
memoized = {}

def combinations(n=200):
  # Pretty sure this is O(2^n)
  
  if n in memoized:
    return memoized[n]
  
  combos = []
  
  for coin in coins:
    remainder = n - coin
    if remainder > 0:
      r_combos = combinations(remainder)
      for combo in r_combos:
        new_combo = combo.copy()
        new_combo[coin] += 1
        if new_combo not in combos:
          combos.append(new_combo)
    elif remainder == 0:
      combos.append(Counter({n: 1}))
  
  sys.stdout.write('\rCompleted up to ' + str(n))
  sys.stdout.flush()
  
  memoized[n] = combos
  return combos

print('\nTotal combinations:', len(combinations()))
