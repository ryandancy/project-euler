#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 1:

If we list all the natural numbers below 10 that are multiples of 3 or 5,
we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""

# Add multiples of 3 to multiples of 5 which are not also multiples of 3
sum_ = sum(range(0, 1000, 3)) + sum(filter(lambda m: m % 3 != 0, range(0, 1000, 5)))
print(sum_)
