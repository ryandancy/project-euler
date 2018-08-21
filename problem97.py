#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 97:

The first known prime found to exceed one million digits was discovered in 1999, and is a Mersenne prime of the form
2^6972593−1; it contains exactly 2,098,960 digits. Subsequently other Mersenne primes, of the form 2^p−1, have been
found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 28433×2^7830457+1.

Find the last ten digits of this prime number.
"""

# Straightforward, calculates it modulo 10^10
# Runs in ~3 seconds

EXPONENT = 7830457
LIMIT = 10**10

# Calculate the last ten digits of 2^7830457
value = 1
for _ in range(EXPONENT):
  value = (value * 2) % LIMIT

# Manipulate the rest
value = ((28433 * value) + 1) % LIMIT

# Left-pad with zeros just in case there are leading zeros
print(str(value).zfill(10))
