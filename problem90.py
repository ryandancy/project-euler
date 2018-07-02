#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 90:

Each of the six faces on a cube has a different digit (0 to 9) written on it; the same is done to a second cube. By
placing the two cubes side-by-side in different positions we can form a variety of 2-digit numbers.

For example, the square number 64 could be formed:

[6] [4]

In fact, by carefully choosing the digits on both cubes it is possible to display all of the square numbers below
one-hundred: 01, 04, 09, 16, 25, 36, 49, 64, and 81.

For example, one way this can be achieved is by placing {0, 5, 6, 7, 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the
other cube.

However, for this problem we shall allow the 6 or 9 to be turned upside-down so that an arrangement like {0, 5, 6, 7, 8,
9} and {1, 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed; otherwise it would be impossible to obtain
09.

In determining a distinct arrangement we are interested in the digits on each cube, not the order.

{1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
{1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}

But because we are allowing 6 and 9 to be reversed, the two distinct sets in the last example both represent the
extended set {1, 2, 3, 4, 5, 6, 9} for the purpose of forming 2-digit numbers.

How many distinct arrangements of the two cubes allow for all of the square numbers to be displayed?
"""

# Generate distinct arrangements (with adding 6/9, etc.), check if each of them can display all squares
# Very efficient, runs in ~377 ms

from itertools import combinations

def generate_die(up_to=None):
  for combo in combinations(map(str, range(10)), 6):
    res = combo
    if '6' in combo:
      res = (*res, *(('9',) * combo.count('6')))
    if '9' in combo:
      res = (*res, *(('6',) * combo.count('9')))
    
    yield res
    
    if up_to and res == up_to:
      break

def can_all_be_displayed(die1, die2):
  can_display = {'01': False, '04': False, '09': False, '16': False, '25': False,
                 '36': False, '49': False, '64': False, '81': False}
  
  for a, b in ((die1, die2), (die2, die1)):
    for num in can_display.keys():
      can_display[num] = can_display[num] or (num[0] in a and num[1] in b)
  
  return all(can_display.values())

print(sum(can_all_be_displayed(die1, die2) for die1 in generate_die() for die2 in generate_die(die1)))
