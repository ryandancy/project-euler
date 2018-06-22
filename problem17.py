#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 17:

If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19
letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one
hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
"""

# Skip translating to letters and go directly to the letter count

# The digit in the ones place to the number of letters in its word (e.g. 1 -> "one" -> 3)
ONES_DIGIT_TO_LETTER_COUNT = {0: 0, 1: 3, 2: 3, 3: 5, 4: 4, 5: 4, 6: 3, 7: 5, 8: 5, 9: 4}

# The digit in the tens place to the number of letters in its word (e.g. 2 -> "twenty" -> 6)
TENS_DIGIT_TO_LETTER_COUNT = {0: 0, 1: 3, 2: 6, 3: 6, 4: 5, 5: 5, 6: 5, 7: 7, 8: 6, 9: 6}

# Special cases: 10-19 ("teens"), by last digit
TEENS_TO_LETTER_COUNT = {0: 3, 1: 6, 2: 6, 3: 8, 4: 8, 5: 7, 6: 7, 7: 9, 8: 8, 9: 8}

# Zeroes in the above dicts are to not add any letters when the digit is 0 (e.g. 40 should add 0 for the ones place)

def number_to_letter_count(n):
  if n == 1000:
    return 11 # "one thousand"
  
  digits = list(map(int, str(n)))[::-1] # reversed so least significant is on top
  
  if len(digits) >= 2 and digits[1] == 1:
    # "teens"
    count = TEENS_TO_LETTER_COUNT[digits[0]]
  else:
    count = ONES_DIGIT_TO_LETTER_COUNT[digits[0]]
    
    if len(digits) > 1:
      # there's a tens digit
      count += TENS_DIGIT_TO_LETTER_COUNT[digits[1]]
  
  if len(digits) > 2:
    # there's a hundreds digit - add the ones equivalent plus 7 ("hundred") or 10 ("hundred and")
    count += ONES_DIGIT_TO_LETTER_COUNT[digits[2]] + (7 if n % 100 == 0 else 10)
  
  return count

print(sum(map(number_to_letter_count, range(1, 1001))))
