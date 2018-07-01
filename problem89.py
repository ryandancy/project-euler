#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 89:

For a number written in Roman numerals to be considered valid there are basic rules which must be followed. Even though
the rules allow some numbers to be expressed in more than one way there is always a "best" way of writing a particular
number.

For example, it would appear that there are at least six ways of writing the number sixteen:

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

However, according to the rules only XIIIIII and XVI are valid, and the last example is considered to be the most
efficient, as it uses the least number of numerals.

The 11K text file, data/p089_roman.txt, contains one thousand numbers written in valid, but not necessarily minimal,
Roman numerals.

Find the number of characters saved by writing each of these in their minimal form.

Note: You can assume that all the Roman numerals in the file contain no more than four consecutive identical units.
"""

# Translate each numeral into an integer, convert that integer into the minimal Roman numeral, subtract lens

ROMANS_TO_INT = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}

def roman_to_int(roman):
  # go through it backwards, adding or subtracting depending on position
  result = 0
  max_seen = 0
  
  for char in reversed(roman):
    value = ROMANS_TO_INT[char]
    if value < max_seen:
      # going down: subtract
      result -= value
    else:
      # not going down: add
      result += value
      
      if value > max_seen:
        max_seen = value
  
  return result

def roman_digit(n, value, digit, five, ten, recurse=True):
  times = n // value
  
  if 1 <= times <= 3:
    roman = digit * times
  elif times == 4:
    roman = digit + five
  elif 5 <= times <= 8:
    roman = five + (digit * (times - 5))
  elif times == 9:
    roman = digit + ten
  else:
    return False
  
  return roman + int_to_roman(n % value) if recurse else roman

def int_to_roman(n):
  # Recursive, hardcoded but it's not too long so whatever
  
  m = n // 1000
  if m:
    return ('M' * m) + int_to_roman(n % 1000)
  
  return (roman_digit(n, 100, 'C', 'D', 'M')
       or roman_digit(n, 10, 'X', 'L', 'C')
       or roman_digit(n, 1, 'I', 'V', 'X', recurse=False)
       or '')

with open('data/p089_roman.txt', 'r') as romans_file:
  romans = map(str.strip, romans_file.readlines())

print(sum(len(roman) - len(int_to_roman(roman_to_int(roman))) for roman in romans))
