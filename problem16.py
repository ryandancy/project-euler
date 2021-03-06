#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 16:

2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?
"""

# Brute force, but using bitshifting because that's cool

print(sum(map(int, str(1 << 1000))))
