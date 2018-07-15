#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 92:

A number chain is created by continuously adding the square of the digits in a number to form a new number until it has
been seen before.

For example,

44 → 32 → 13 → 10 → 1 → 1
85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY
starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
"""

# Straightforward: memoize whether each chain arrives at 1 or 89
# Runs in ~1 minute

def next_in_chain(prev):
  return sum(map(lambda digit: int(digit)**2, str(prev)))

memoized = {1: False, 89: True}
def arrives_at_89(n):
  if n not in memoized:
    memoized[n] = arrives_at_89(next_in_chain(n))
  return memoized[n]

if __name__ == '__main__':
  print(sum(map(arrives_at_89, range(1, 10000000))))
