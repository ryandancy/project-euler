#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 42:

The nth term of the sequence of triangle numbers is given by, t(n) = ½n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we
form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t(10). If the word value is a triangle
number then we shall call the word a triangle word.

Using data/p042_words.txt, a 16K text file containing nearly two-thousand common English words, how many are triangle
words?
"""

'''
It can be shown that when t is a triangle number (i.e. t = n(n+1)/2 for some whole number n), sqrt(8t + 1) is an odd
integer:

t = n(n+1)/2
2t = n^2 + n
n^2 + n - 2t = 0
n = (-1 + sqrt(1^2 - 4*1*-2t))/(2*1)   (ignoring minus because n > 0)
n = (-1 + sqrt(8t + 1))/2
n = -1/2 + sqrt(8t + 1)/2
2n = -1 + sqrt(8t + 1)
2n + 1 = sqrt(8t + 1)

But 2n + 1 for some natural number n is the definition of a positive odd number.
Therefore sqrt(8t + 1) is odd when t = n(n+1)/2 for some whole number n (i.e. t is a triangle number).

Using this, calculate the word values and whether they are triangle words. Very fast: 88ms for all 2000+ words.
'''

from math import sqrt
from ast import literal_eval

def is_triangle(t):
  result = sqrt(8*t + 1) % 2 == 1
  return result

def get_score(word):
  return sum(ord(c) - 64 for c in word) # ord('A') == 65

with open('data/p042_words.txt') as words_file:
  words = literal_eval(words_file.read())

num_triangles = 0
for word in words:
  if is_triangle(get_score(word)):
    num_triangles += 1

print(num_triangles)
