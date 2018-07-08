#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 58:

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting is that
8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed. If this
process is continued, what is the side length of the square spiral for which the ratio of primes along both diagonals
first falls below 10%?
"""

from math import sqrt

def is_prime(n):
  for divisor in range(2, int(sqrt(n)) + 1):
    if n % divisor == 0:
      return False
  return True

all_primes = set()
start_generating_primes_at = 2

def populate_primes_up_to(n): # inclusive
  global start_generating_primes_at
  
  for p in range(start_generating_primes_at, n + 1):
    for prime in all_primes:
      if p % prime == 0:
        break
    else:
      all_primes.add(p)
  
  start_generating_primes_at = n + 1

primes = 0
total = 1 # including 1
side_length = 1
currently_adding = 0
last = 1

while primes / total >= 0.1 or primes == 0:
  if side_length % 100 == 1:
    print(side_length, primes / total, primes, total, last)
  
  side_length += 2
  currently_adding += 2
  
  new_last = last + currently_adding * 4
  
  #populate_primes_up_to(new_last)
  
  for diagonal in range(last + currently_adding, new_last + 1, currently_adding):
    if is_prime(diagonal): #diagonal in all_primes:
      primes += 1
  
  total += 4
  last = new_last

print(side_length)
