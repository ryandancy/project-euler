#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 79:

A common security method used for online banking is to ask the user for three random characters from a passcode. For
example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be:
317.

The text file, data/p079_keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible
secret passcode of unknown length.
"""

# Generate a graph of which digits must be before which from the keylogs, generate all passwords until one fits
# Finds the optimal solution for the dataset in ~2 minutes

from sys import exit
from itertools import product, count
from collections import defaultdict

def valid(pwd, pwd_graph):
  try:
    for key, values in pwd_graph.items():
      first_key_index = pwd.index(key)
      for value in values:
        if first_key_index > pwd.rindex(value):
          return False
  except ValueError:
    return False
  else:
    return True

if __name__ == '__main__':
  with open('data/p079_keylog.txt', 'r') as keylog_file:
    keylogs = map(tuple, keylog_file.readlines())

  pwd_graph = defaultdict(lambda: set())

  for n0, n1, n2, _ in keylogs:
    pwd_graph[n0].add(n1)
    pwd_graph[n1].add(n2)

  for i in count(1):
    for pwd in product(map(str, range(10)), repeat=i):
      if valid(''.join(pwd), pwd_graph):
        print(''.join(pwd))
        exit(0)
