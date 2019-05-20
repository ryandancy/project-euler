#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 112:

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for
example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525)
are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy numbers
is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.
"""

# Simple brute-force method

def is_bouncy(n):
  digits = list(map(int, str(n)))
  is_inc = True
  is_dec = True
  for dig1, dig2 in zip(digits, digits[1:]):
    if is_inc and dig1 > dig2:
      is_inc = False
    if is_dec and dig1 < dig2:
      is_dec = False
    if not (is_inc or is_dec):
      return True
  return False

non_bouncy = 1
bouncy = 0
n = 2
while non_bouncy * 99 != bouncy: # integer version of bouncy / (non_bouncy + bouncy) != 0.99
  if is_bouncy(n):
    bouncy += 1
  else:
    non_bouncy += 1
  n += 1

print(n - 1)
