#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 33:

The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly
believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits
in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
"""

from fractions import Fraction
from collections import Counter

product_fraction = Fraction(1, 1)

for denom in range(10, 100):
  for numer in range(10, denom):
    if numer == denom:
      continue
    
    numer_digits = Counter(map(int, str(numer)))
    denom_digits = Counter(map(int, str(denom)))
    
    # find the common digit
    common_digit = numer_digits & denom_digits
    if len(common_digit) != 1 or list(common_digit)[0] == 0:
      # if the common digit is 0, it's trivial
      continue
    
    # cancel the common_digit, do the fractions match?
    other_numer_digit = list(numer_digits - common_digit)[0]
    other_denom_digit = list(denom_digits - common_digit)[0]
    
    try:
      this_fraction = Fraction(numer, denom)
      cancelled_fraction = Fraction(other_numer_digit, other_denom_digit)
    except ZeroDivisionError:
      # if one of the denominators is 0 they obviously aren't equal
      continue
    
    if this_fraction != cancelled_fraction:
      continue
    
    # update the product fraction
    print('Found: {}/{}'.format(numer, denom))
    product_fraction *= this_fraction

print('Product of fractions:', product_fraction)
print('Denominator:', product_fraction.denominator)
