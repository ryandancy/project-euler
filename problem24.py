#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 24:

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3
and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The
lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
"""

# Use the built-in permutation generator in itertools
# next(islice(generator, n, None)) takes the nth (zero-indexed) = (n+1)th (one-indexed) element generated by generator

from itertools import permutations, islice

print(''.join(next(islice(permutations('0123456789'), 999999, None))))
