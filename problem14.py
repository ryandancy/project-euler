#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 14:

The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

# Memoize the chain lengths to avoid recalculating them each time

chain_lengths = {1: 0}

def get_chain_length(n):
  try:
    return chain_lengths[n]
  except KeyError:
    if n % 2 == 0:
      real_length = get_chain_length(n // 2) + 1
    else:
      real_length = get_chain_length(3*n + 1) + 1
    
    chain_lengths[n] = real_length
    return real_length

longest_chain = 0

for n in range(2, 1000001):
  length = get_chain_length(n)
  if length > longest_chain:
    longest_chain = length
    longest_num = n

print(longest_num)
