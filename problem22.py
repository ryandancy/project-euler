#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 22:

Using data/p022_names.txt, a 46K text file containing over five-thousand first names, begin by sorting it into
alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical
position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the
938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
"""

from ast import literal_eval

with open('data/p022_names.txt') as names_file:
  names = list(literal_eval(names_file.read()))

names.sort()

score_total = 0
for i, name in enumerate(names):
  score_total += (i + 1) * sum(ord(char) - ord('A') + 1 for char in name)

print(score_total)
