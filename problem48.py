#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 48:

The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""

# Calculate the powers manually, throwing away everything except the last 10 digits
# Python could probably handle the full power but whatever

full_sum = 0

for n in range(1, 1001):
  n_product = 1
  
  for _ in range(n):
    n_product *= n
    n_product %= 10**10
  
  full_sum += n_product

print(full_sum % 10**10)
