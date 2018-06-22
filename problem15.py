#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 15:

Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6
routes to the bottom right corner.

How many such routes are there through a 20×20 grid?
"""

# In Pascal's Triangle, each number can be seen to represent the number of paths to that number starting at the top.
# Therefore, the bottommost node of a square on Pascal's Triangle starting at the top is the number of paths to reach
# that node from the top node.

# These numbers on Pascal's Triangle are called the central binomial coefficients (http://oeis.org/A000984), and the
# formula for the nth central binomial coefficient is binomial(2*n, n) = (2*n)! / (n!)^2.

from math import factorial

n = 20

print(factorial(2*n) // factorial(n) ** 2)
