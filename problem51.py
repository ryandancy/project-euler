#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 51:

By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53,
73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven
primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993.
Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is
part of an eight prime value family.
"""

from math import sqrt
from collections import defaultdict
from itertools import count, combinations
import sys

memoized = {1: False}
def is_prime(n):
  if n in memoized:
    return memoized[n]
  
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      result = False
      break
  else:
    result = True
    
  memoized[n] = result
  return result

def replace(digits, digit_combo, replacement):
  return ''.join(
    replacement if i in digit_combo else digit
    for i, digit in enumerate(digits)
  )

def are_8_variants_prime(digits, digit_combo):
  prime_variants = 0
  
  # don't replace the start of a number with 0
  replacement_values = '123456789' if 0 in digit_combo else '0123456789'
  
  for replacement in replacement_values:
    variant = int(replace(digits, digit_combo, replacement))
    
    if is_prime(variant):
      prime_variants += 1
      
      if prime_variants >= 8:
        return True
  
  return False

def find_first_8_prime():
  for n in count(2):
    if not is_prime(n):
      continue
    
    digits = str(n)
    
    # find digits that are the same
    positions_dict = defaultdict(lambda: [])
    for i, digit in enumerate(digits):
      positions_dict[digit].append(i)
    
    replacement_combos = []
    for digit, positions in positions_dict.items():
      for digits_to_replace in range(1, len(positions) + 1):
        replacement_combos += list(combinations(positions, digits_to_replace))
    
    sys.stdout.write('\rChecking: ' + digits)
    
    for digit_combo in replacement_combos:
      if are_8_variants_prime(digits, digit_combo):
        return n # the smallest

print('\nFirst prime with 8 prime replacements: {}'.format(find_first_8_prime()))
