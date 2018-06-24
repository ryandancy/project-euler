#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 40:

An irrational decimal fraction is created by concatenating the positive integers:

0.12345678910(1)112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If d(n) represents the nth digit of the fractional part, find the value of the following expression.

d(1) × d(10) × d(100) × d(1000) × d(10000) × d(100000) × d(1000000)
"""

# Keep track of indices into counter only

counter = 0
looking_for = [1, 10, 100, 1000, 10000, 100000, 1000000]
product = 1
up_to = max(looking_for)

n = 1
while n <= up_to:
  s = str(n)
  for index in looking_for:
    if counter < index and counter + len(s) >= index:
      product *= int(s[index - counter - 1])
      break
  counter += len(s)
  n += 1

print(product)
