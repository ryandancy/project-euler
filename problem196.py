#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 196:

Build a triangle from all positive integers in the following way:

 1
 2  3
 4  5  6
 7  8  9 10
11 12 13 14 15
16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31 32 33 34 35 36
37 38 39 40 41 42 43 44 45
46 47 48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63 64 65 66
. . .

Each positive integer has up to eight neighbours in the triangle.

A set of three primes is called a prime triplet if one of the three primes has the other two as neighbours in the
triangle.

For example, in the second row, the prime numbers 2 and 3 are elements of some prime triplet.

If row 8 is considered, it contains two primes which are elements of some prime triplet, i.e. 29 and 31.
If row 9 is considered, it contains only one prime which is an element of some prime triplet: 37.

Define S(n) as the sum of the primes in row n which are elements of any prime triplet.
Then S(8)=60 and S(9)=37.

You are given that S(10000)=950007619.

Find S(5678027) + S(7208785).
"""

# We find all primes in the rows 2 above to 2 below, then look for prime triplets in the middle row
# Runs in ~2 minutes

from time import clock
from itertools import compress

# Note: assumes range does *not* include 2 because it's not necessary for this problem
def primes_in_range(n1, n2): # inclusive
  # Based off Michael M. Ross' answer at https://bit.ly/2wisbkK
  # We build a list mapping odd numbers in the interval [n1, n2] to whether or not they're prime
  # We then go through every (ish) combination of two odd factors to find all composite numbers; the rest are prime
  
  # Make n1 odd
  if n1 % 2 == 0:
    n1 += 1
  
  # odd_map[i] = is 2*i + n1 prime?
  odd_map = [True] * ((n2 - n1) // 2 + 1)
  m = 3
  f = 5
  
  while f != 3 and m <= f:
    f = n1 // m
    if f % 2 == 0:
      f += 1
    if f < 3:
      f = 3
    
    mf = m*f
    
    while mf <= n2:
      if mf > n1:
        idx = (mf - n1) // 2
        if odd_map[idx]:
          odd_map[idx] = False
      f += 2
      mf = m*f
    
    m += 2
  
  return set(compress(range(n1, n2+1, 2), odd_map))

def neighbours(n, row, min_row, max_row): # returns list of (row, num)
  if n == min_row:
    return [(row - 1, n - row + 1), (row - 1, n - row + 2), (row, n + 1), (row + 1, n + row), (row + 1, n + row + 1)]
  elif n == max_row:
    return [(row - 1, n - row), (row + 1, n + row + 1), (row + 1, n + row), (row + 1, n + row - 1), (row, n - 1)]
  elif n == max_row - 1:
    return [(row - 1, n - row), (row - 1, n - row + 1), (row, n + 1), (row + 1, n + row + 1), (row + 1, n + row),
            (row + 1, n + row - 1), (row, n - 1)]
  else:
    return [(row - 1, n - row), (row - 1, n - row + 1), (row - 1, n - row + 2), (row, n + 1), (row + 1, n + row + 1),
            (row + 1, n + row), (row + 1, n + row - 1), (row, n - 1)]

def sum_prime_triplet_members(row):
  # Max in row n is the nth triangular number - n(n+1)/2
  max_row = row * (row + 1) // 2
  
  # Min in row n is the max minus n plus 1
  min_row = max_row - row + 1
  
  # Make min_row odd
  if min_row % 2 == 0:
    min_row += 1
  
  total = 0
  
  min_possible_neigh = (row - 2) * (row - 1) // 2 - row + 3
  max_possible_neigh = (row + 2) * (row + 3) // 2
  print('Finding primes between {} and {} ({} to check)...'.format(
    min_possible_neigh, max_possible_neigh, max_possible_neigh - min_possible_neigh))
  timestamp = clock()
  primes = primes_in_range(min_possible_neigh, max_possible_neigh)
  print('There are {} primes between {} and {} (took {} s)'.format(
    len(primes), min_possible_neigh, max_possible_neigh, clock() - timestamp))
  
  for n in range(min_row, max_row + 1, 2):
    if n not in primes:
      continue
    
    neighs = neighbours(n, row, min_row, max_row)
    
    found_prime = False
    prime_neighbour = None
    found_all_primes = False
    
    # Try to find 2 primes among neighbours
    for neighbour in neighs:
      if neighbour[1] % 2 == 1 and neighbour[1] in primes:
        if found_prime:
          # We found both primes
          total += n
          found_all_primes = True
          break
        else:
          # We found the first prime
          prime_neighbour = neighbour
          found_prime = True
    
    if found_all_primes:
      continue
    elif found_prime:
      # We only found one prime - check its neighbours for another prime
      neigh_row, neigh = prime_neighbour
      
      max_neigh_row = neigh_row * (neigh_row + 1) // 2
      min_neigh_row = max_neigh_row - neigh_row + 1
      
      excluded_neighbours = [*neighs, (row, n)]
      
      neighbour_neighbours = neighbours(neigh, neigh_row, min_neigh_row, max_neigh_row)
      for neighbour2 in neighbour_neighbours:
        if neighbour2[1] % 2 == 1 and neighbour2 not in excluded_neighbours and neighbour2[1] in primes:
          total += n
          break
  
  print('Result:', total)
  
  return total

print(sum_prime_triplet_members(5678027) + sum_prime_triplet_members(7208785))
