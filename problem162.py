#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 162:

In the hexadecimal number system numbers are represented using 16 different digits:

0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F

The hexadecimal number AF when written in the decimal number system equals 10x16+15=175.

In the 3-digit hexadecimal numbers 10A, 1A0, A10, and A01 the digits 0,1 and A are all present.
Like numbers written in base ten we write hexadecimal numbers without leading zeroes.

How many hexadecimal numbers containing at most sixteen hexadecimal digits exist with all of the digits 0, 1, and A
present at least once?
Give your answer as a hexadecimal number.

(A, B, C, D, E and F in upper case, without any leading or trailing code that marks the number as hexadecimal and
without leading zeroes, e.g. 1A3F and not: 1a3f and not 0x1a3f and not $1A3F and not #1A3F and not 0000001A3F)
"""

from functools import reduce
from itertools import permutations
from math import factorial
import operator

def choose(x, y):
  try:
    return factorial(x) // factorial(y) // factorial(x - y)
  except ValueError:
    return 0

def num_permutations_repeated(total, *combo):
  return factorial(total) // reduce(operator.mul, map(factorial, combo))

def partitions(n, partition_len, min_part=1):
  # https://stackoverflow.com/a/18503391/8468108
  if partition_len == 1:
    if n >= min_part:
      yield (n,)
    return
  
  for i in range(min_part, n + 1):
    for result in partitions(n - i, partition_len - 1, i):
      yield (i, *result)

def gen_01A():
  # (0, 1, A) represented by (0, 1, 2)
  for length in range(3, 17):
    for partition in partitions(length, 3):
      yield from set(permutations(partition))

def num_combos(total01A, always_on_left):
  this_total = 0
  
  for free in range(17 - total01A):
    num_placements = 0
    
    for on_left in range(always_on_left, free + 1):
      for on_right in range(free - on_left + 1):
        num_placements += choose(total01A - 1, free - on_left - on_right)
    
    # print('For', total01A, 'total with', free, 'free, there are', num_placements, 'placements')
    
    this_total += num_placements * 13**free
  
  return this_total

total = 0

for combo in gen_01A():
  #print(combo)
#  print(''.join({0: '0', 1: '1', 2: 'A'}[x] * n for n, x in combo))
  
  total01A = sum(combo)#combo[0][0] + combo[1][0] + combo[2][0]
  #  print('total 0, 1, A:', total01A)
  
  not_start_zero = num_combos(total01A, False)
  # print('not starting zero:', not_start_zero)
  start_zero = num_combos(total01A, True)
  # print('starting zero:', start_zero)
  
  total_permutations = num_permutations_repeated(total01A, *combo)
  # total_starting_zero = sum(
  #   (c * total_permutations // total01A) for c in set(combo)
  # )
  total_starting_zero = combo[0] * total_permutations // total01A
  total_not_starting_zero = total_permutations - total_starting_zero
  
  print(combo, '| total:', total_permutations, '| starting 0:', total_starting_zero, '| not starting 0:', 
        total_not_starting_zero)
  
  total += total_starting_zero * start_zero + total_not_starting_zero * not_start_zero
  
  # this_total = 0
  
  # for free in range(17 - total01A):
  #   num_placements = 0
    
  #   # leading zeroes require that there's always one on the left
  #   always_on_left = 1 if combo[0] == 0 else 0
    
  #   for on_left in range(always_on_left, free + 1):
  #     for on_right in range(free - on_left + 1):
  #       num_placements += choose(total01A - 1, free - on_left - on_right)
    
  #   this_total += num_placements * 13**free
#    print('with', free, 'free, there are', num_placements, 'placements')
  
  # total += this_total

print(total)
print(hex(total)[2:].upper())
