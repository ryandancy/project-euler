#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 25:

The Fibonacci sequence is defined by the recurrence relation:

F(n) = F(n−1) + F(n−2), where F(1) = 1 and F(2) = 1.
Hence the first 12 terms will be:

F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34
F(10) = 55
F(11) = 89
F(12) = 144
The 12th term, F(12), is the first term to contain three digits.

What is the index of the first term in the Fibonacci sequence to contain 1000 digits?
"""

# Brute force: use a generator to get the Fibonacci numbers and next() to find the first with 1000 digits

def fibonacci():
  index = 1
  current = 1
  last = 0
  
  while True:
    yield index, current
    current, last = current + last, current
    index += 1

print(next(idx for idx, num in fibonacci() if len(str(num)) == 1000))
