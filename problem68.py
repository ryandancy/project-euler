#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 68:

Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.

Working clockwise, and starting from the group of three with the numerically lowest external node (4,3,2 in this
example), each solution can be described uniquely. For example, the above solution can be described by the set: 4,3,2;
6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight solutions in total.

Total	     Solution Set
9       4,2,3; 5,3,1; 6,1,2
9       4,3,2; 6,2,1; 5,1,3
10      2,3,5; 4,5,1; 6,1,3
10      2,5,3; 6,3,1; 4,1,5
11      1,4,6; 3,6,2; 5,2,4
11      1,6,4; 5,4,2; 3,2,6
12      1,5,6; 2,6,4; 3,4,5
12      1,6,5; 3,5,4; 2,4,6
By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings. What is the
maximum 16-digit string for a "magic" 5-gon ring?
"""

# Let the outer ring be a_1 through a_5 and the inner ring be b_1 through b_5
# We iterate the "magic" number, generate a_1, generate possible b_1 and b_2, generate possible a_2 and b_3 from b_2,
# etc. If the generated b_1 after 5 iterations is the same as the original b_1, it is a solution.
# This solution runs in ~0.12 seconds.

from itertools import count, starmap

NGON = 5

def len2_partitions(n):
  for m in range(1, n):
    yield n - m, m

def gen_for_magic_and_b(magic, this_b, original_b, a, b, to_go=NGON-2):
  if to_go == 0:
    a5 = magic - this_b - original_b
    if 10 >= a5 > 0 and a5 not in a and a5 not in b:
      yield [*a, a5], b
    return
  
  for this_a, b2 in len2_partitions(magic - this_b):
    if b2 >= 10 or this_a > 10 or this_a in a or this_a in b or b2 in a or b2 in b:
      continue
    
    yield from gen_for_magic_and_b(magic, b2, original_b, [*a, this_a], [*b, b2], to_go - 1)

def gen_for_magic(magic):
  for a1 in range(1, 11):
    for b1, b2 in len2_partitions(magic - a1):
      if b1 >= 10 or b2 >= 10 or a1 == b1 or a1 == b2 or b1 == b2:
        continue
      yield from gen_for_magic_and_b(magic, b2, b1, [a1], [b1, b2])

def get_digit_string(a, b):
  shift = a.index(min(a))
  result = ''
  for i in range(NGON):
    result += str(a[(i+shift)%NGON]) + str(b[(i+shift)%NGON]) + str(b[(i+shift+1)%NGON])
  return int(result)

highest = -1
for magic in count(13):
  try:
    this_highest = max(starmap(get_digit_string, gen_for_magic(magic)))
    if this_highest > highest:
      highest = this_highest
  except ValueError:
    # max() didn't have anything - no magic strings left
    break

print(highest)
