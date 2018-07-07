#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 57:

It is possible to show that the square root of two can be expressed as an infinite continued fraction.

√2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985, is the first example
where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than denominator?
"""

# If e_n is the nth expansion, e_n = 1 + 1(1 + e_{n-1})
# Using this, keep track of the expansions throughout; runs in ~150 ms

from fractions import Fraction

total = 0
expansion = Fraction(3, 2)

for n in range(2, 1000):
  expansion = 1 + 1/(1 + expansion)
  
  numer, denom = expansion.numerator, expansion.denominator
  digits_numer, digits_denom = len(str(numer)), len(str(denom))
  
  if digits_numer > digits_denom:
    total += 1

print(total)
