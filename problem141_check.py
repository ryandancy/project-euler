#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file validates the solutions for problem 141 in the file with the name of the first command-line argument and
outputs the new sum once all invalid solutions have been rejected. This was used to derive the correct answer from the
superset of valid solutions previously output by problem141.py.
"""


from typing import Tuple
from math import sqrt
import sys


def get_filename():
  try:
    return sys.argv[1]
  except IndexError:
    return input('Filename in which to validate solutions: ')


def is_valid(r, d, n) -> Tuple[bool, str]: # (is valid, reason)
  # n must be a perfect square
  if not sqrt(n).is_integer():
    return False, '{} is not a perfect square'.format(n)
  
  # n/d must have remainder r
  q, r2 = divmod(n, d)
  if r != r2:
    return False, '{}/{} did not have remainder {}'.format(n, d, r)
  
  # r, q, d (not in that order) must form a geometric sequence
  geometric = sorted([r, d, q])
  if geometric[2] / geometric[1] != geometric[1] / geometric[0]:
    return False, '({}, {}, {}) did not form a geometric sequence'.format(*geometric)
  
  return True, 'valid'


def main():
  try:
    with open(get_filename(), 'r') as file_to_check:
      lines = file_to_check.readlines()
  except FileNotFoundError:
    print('File did not exist!')
  
  new_sum = 0
  
  for line_num, line in enumerate(lines):
    try:
      line_tuple = tuple(map(int, line.strip().split()))
      r, d, n = line_tuple[:3] # disregard 4th if it exists (cube)
    except Exception as e:
      print('Bad format:', e)
    
    valid, msg = is_valid(r, d, n)
    if valid:
      new_sum += n
    else:
      print('Line {} ({}, {}, {}) rejected for reason: {}'.format(line_num, r, d, n, msg))
  
  print('New sum:', new_sum)


if __name__ == '__main__':
  main()
