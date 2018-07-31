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

'''
This solution generates all possible numbers of A, 1, and 0 in one hex number up to 16; i.e. it generates (1, 1, 1)
for 1 A, 1 1, and 1 0, then (1, 2, 1) for 1 A, 2 1s, and 1 0, et cetera. This is equivalent to the length-3 compositions
of each number 3 through 16 inclusive (which is equivalent to the distinct permutations of those numbers).

For each of these combinations, the first number is interpreted as the number of zeroes. Let t be the total number of
As, 1s, and 0s; the number of hex numbers (up to 16 total digits) with t known digits is calculated like so:

Let g(f, t) be the number of possible placements of f unknown digits onto t known digits.
g(f, t) = 0 for f < 0
g(0, t) = 1
g(f, t) = sum_{n=1}^t g(f-1, n)
The number of hex numbers with t known digits is sum_{f=0}^{16-t} g(f, t)*13^f. 13 is chosen as it is the number of
possible hex values for a digit excluding 0, 1, and A.

If the first digit of A, 1, and 0 is 0, 1 is subtracted from f to signify that there must always be a digit before the
first digit so that the first A/1/0 digit may be 0.

The number of hex numbers with the total number of digits is calculated, both for with a leading 0 and without. The
number of permutations of the partition (e.g. (1, 2, 1)) is calculated with the formula t! / (x!y!z!), where (x, y, z)
is the partition. Of that total number of permutations, if x is the number of zeroes, x/t of the permutations begin with
zero, and the rest do not. This is used to calculate the number of hex numbers with the given number of As, 1s, and 0s,
which is then summed with the values for the rest of the compositions to give the result, which is converted to hex.

This solution runs in ~0.1 seconds.
'''

from functools import reduce
from itertools import permutations
from math import factorial
import operator

DIGIT_LIMIT = 16

def num_permutations_repeated(total, combo):
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
  for length in range(3, DIGIT_LIMIT + 1):
    for partition in partitions(length, 3):
      yield from set(permutations(partition))

memoized = {}
def get_num_placements(total01A, free, always_on_left):
  if always_on_left:
    free -= 1
  
  if free < 0:
    return 0
  if free == 0:
    return 1
  if free == 1:
    return total01A + 1
  
  if (total01A, free) not in memoized:
    memoized[(total01A, free)] = sum(get_num_placements(n, free - 1, False) for n in range(total01A + 1))
  return memoized[(total01A, free)]

def num_combos(total01A, always_on_left):
  this_total = 0
  
  for free in range(DIGIT_LIMIT - total01A + 1):
    num_placements = get_num_placements(total01A, free, always_on_left)
    this_total += num_placements * 13**free
  
  return this_total

total = 0

for combo in gen_01A(): # combo is num of (0, 1, A)
  total01A = sum(combo)
  
  not_start_zero = num_combos(total01A, False)
  start_zero = num_combos(total01A, True)
  
  total_permutations = num_permutations_repeated(total01A, combo)
  total_starting_zero = combo[0] * total_permutations // total01A
  total_not_starting_zero = total_permutations - total_starting_zero
  
  total += total_starting_zero * start_zero + total_not_starting_zero * not_start_zero

print(hex(total)[2:].upper())
