#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 6:

1^2 + 2^2 + ... + 10^2 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)^2 = 552 = 3025
Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is
3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
"""

# brute force for the sum of squares, Gauss' summation formula for the square of the sum

n = 100

sum_of_squares = sum(x ** 2 for x in range(1, n + 1))
square_of_sum = ((n * (n + 1)) // 2) ** 2

print(abs(sum_of_squares - square_of_sum))
