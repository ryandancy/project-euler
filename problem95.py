#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 95:

The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of 28
are 1, 2, 4, 7, and 14. As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220, forming a
chain of two numbers. For this reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496, we form a chain of five numbers:

12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.
"""

# Fairly straightforward
# Runs in ~4 minutes

from math import sqrt

LIMIT = 10**6

def sum_of_divisors(n):
  result = 1
  for d in range(2, int(sqrt(n)) + 1):
    d2, mod = divmod(n, d)
    if mod == 0:
      if d == d2:
        result += d
      else:
        result += d + d2
  return result

chain_lengths = {1: 0}

for n in range(2, LIMIT + 1):
  if n % 1000 == 0:
    print(n)
  
  if n in chain_lengths:
    continue
  
  chain = [n]
  current = sum_of_divisors(n)
  
  while True:
    if current > LIMIT:
      for elem in chain:
        chain_lengths[elem] = 0
      break
    elif current in chain:
      pos = chain.index(current)
      repeat_len = len(chain) - pos
      
      for elem in chain[pos:]:
        chain_lengths[elem] = repeat_len
      
      for elem in chain[:pos]:
        chain_lengths[elem] = 0
      
      break
    elif current in chain_lengths:
      for elem in chain:
        chain_lengths[elem] = 0
      break
    
    chain.append(current)
    current = sum_of_divisors(current)

longest_chain_length = max(chain_lengths.values())
longest_chain_start = next(n for n, length in chain_lengths.items() if length == longest_chain_length)

# find smallest member of chain
smallest = longest_chain_start
chain = [longest_chain_start]
current = sum_of_divisors(smallest)

while True:
  if current < smallest:
    smallest = current
  
  if current in chain:
    break
  
  chain.append(current)
  current = sum_of_divisors(current)

print(smallest)
print(chain)
