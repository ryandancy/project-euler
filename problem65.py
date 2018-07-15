#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 65:

The square root of 2 can be written as an infinite continued fraction.

√2 = 1 + 1/(2 + 1/(2 + 1/(2 + ...)))

The infinite continued fraction can be written, √2 = [1;(2)], (2) indicates that 2 repeats ad infinitum. In a similar
way, √23 = [4;(1,3,1,8)].

It turns out that the sequence of partial values of continued fractions for square roots provide the best rational
approximations. Let us consider the convergents for √2.

1 +	1/2 = 3/2

1 +	1/(2 + 1/2) = 7/5

1 + 1/(2 + 1/(2 + 1/2)) = 17/12

1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29
 
Hence the sequence of the first ten convergents for √2 are:

1, 3/2, 7/5, 17/12, 41/29, 99/70, 239/169, 577/408, 1393/985, 3363/2378, ...

What is most surprising is that the important mathematical constant,

e = [2; 1,2,1, 1,4,1, 1,6,1 , ... , 1,2k,1, ...].

The first ten terms in the sequence of convergents for e are:

2, 3, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1264/465, 1457/536, ...
The sum of digits in the numerator of the 10th convergent is 1+4+5+7=17.

Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.
"""

# Straightforward; to calculate the nth convergent, work backwards from the last addend
# Runs in ~0.15s

from itertools import count, islice
from fractions import Fraction

def gen_e_terms():
  for n in count(2, 2):
    yield 1
    yield n
    yield 1

def nth_convergent(n, initial, gen_more): # gen_more must be fresh
  # work backwards
  addends = [initial] + list(islice(gen_more, n - 1))
  convergent = Fraction(addends[-1])
  
  for addend in reversed(addends[:-1]):
    convergent = addend + 1/convergent
  
  return convergent

def sum_of_digits(n):
  return sum(map(int, str(n)))

print(sum_of_digits(nth_convergent(100, 2, gen_e_terms()).numerator))
