#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 75:

It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided right angle triangle in
exactly one way, but there are many more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle triangle, and other
lengths allow more than one solution to be found; for example, using 120 cm it is possible to form exactly three
different integer sided right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L ≤ 1,500,000 can exactly one integer sided right angle
triangle be formed?
"""

# Generate Pythagorean triples, check their sums

# http://mathworld.wolfram.com/PythagoreanTriple.html:
# "Hall (1970) and Roberts (1977) prove that (a,b,c) is a primitive Pythagorean triple iff
# (a,b,c)=(3,4,5)M, where M is a finite product of the matrices U, A, D"
# where U = [1, 2, 2; -2, -1, -2; 2, 2, 3], A = [1, 2, 2; 2, 1, 2; 2, 2, 3], D = [-1, -2, -2; 2, 1, 2; 2, 2, 3].
# All Pythagorean triplets can be written as (na, nb, nc) where (a, b, c) is a primitive Pythagorean triplet and
# n is a natural number.

# Runs in ~6 seconds

from collections import defaultdict
import numpy as np

def generate_primitive_triples(sum_limit):
  u = np.mat([[ 1,  2,  2],
              [-2, -1, -2],
              [ 2,  2,  3]])
  a = np.mat([[ 1,  2,  2],
              [ 2,  1,  2],
              [ 2,  2,  3]])
  d = np.mat([[-1, -2, -2],
              [ 2,  1,  2],
              [ 2,  2,  3]])
  
  uad = np.array([u, a, d])
  triples = np.array([[3, 4, 5]])
  
  while triples.size:
    # Remove triples where the sum is too big
    triples = triples[triples.sum(axis=1) <= sum_limit]
    yield from triples
    
    # Generate more triples by multiplying the array by the magic matrices
    triples = np.dot(triples, uad)
    
    # Make the array of triples 2D
    triples = triples.reshape(-1, 3)

sums = defaultdict(lambda: 0)

def process_triple_sums(sum_limit):
  for triple in generate_primitive_triples(sum_limit):
    n = 1
    new_triple = n * triple
    triple_sum = new_triple.sum()
    
    while triple_sum <= sum_limit:
      sums[triple_sum] += 1
      
      n += 1
      new_triple = n * triple
      triple_sum = new_triple.sum()

process_triple_sums(1500000)
print(sum(map(lambda s: sums[s] == 1, sums.keys())))
