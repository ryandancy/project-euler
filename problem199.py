#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 199:

Three circles of equal radius are placed inside a larger circle such that each pair of circles is tangent to one another
and the inner circles do not overlap. There are four uncovered "gaps" which are to be filled iteratively with more tangent circles.

At each iteration, a maximally sized circle is placed in each gap, which creates more gaps for the next iteration. After
3 iterations, there are 108 gaps and the fraction of the area which is not covered by circles is 0.06790342, rounded to
eight decimal places.

What fraction of the area is not covered by circles after 10 iterations?
Give your answer rounded to eight decimal places using the format x.xxxxxxxx.
"""

"""
For this problem, it is easiest to deal with the circles in terms of their curvatures. The curvature of a circle is the
reciprocal of its radius and is usually denoted by k; k = 1/r.

Descartes' theorem states that the curvature k_4 of a circle tangent to three mutually tangent circles with curvatures
k_1, k_2 and k_3 can be found as such:

k_4 = k_1 + k_2 + k_3 + 2√(k_1k_2 + k_2k_3 + k_3k_1)

Our algorithm starts with three curvatures and continually keeps track of the gaps formed by the circles; these gaps
are defined by the three circles that create the gap. For the requisite number of iterations, the algorithm removes a
3-tuple of curvatures (k_1, k_2, k_3) from the list of gaps, calculates the curvature k_4 of the inscribed circle using
Descartes' theorem, adds its area to a running total, then adds (k_4, k_1, k_2), (k_4, k_2, k_3), and (k_4, k_3, k_1) to
the list of gaps.

This algorithm is performed twice: once for the three gaps between the starting circles and the outer circle and once
for the gap between the three circles. The former's resultant area is multiplied by three and added to the latter's
resultant area and three times the area of one of the starting circles, then divided by the area covered by the outer
circle and subtracted from one to get the answer.

Note that the curvature of the outer circle was set to 1, and based on that the curvatures of the starting circles were
found to be (3 + 2√3)/3.

This solution runs in ~0.2 seconds.
"""

from math import sqrt, pi
from itertools import combinations

MAX_ITERATION = 9

K_OUTER = -1 # negative because it's internally tangent
K_STARTING = (3 + 2*sqrt(3)) / 3

def inscribed_curvature(k1, k2, k3):
  # Descartes' theorem
  return k1 + k2 + k3 + 2*sqrt(k1*k2 + k2*k3 + k3*k1)

def area_from_curvature(k):
  r = 1/abs(k)
  return pi*r*r

def amount_filled_in_gap(initial_k1, initial_k2, initial_k3):
  # list of (iteration #, (curvature 1, curvature 2, curvature 3))
  gaps = [(0, (initial_k1, initial_k2, initial_k3))]
  result = 0
  
  while gaps:
    iteration, curvatures = gaps.pop()
    k = inscribed_curvature(*curvatures)
    result += area_from_curvature(k)
    
    if iteration == MAX_ITERATION:
      continue
    
    for other_ks in combinations(curvatures, 2):
      gaps.append((iteration + 1, (k, *other_ks)))
  
  return result

filled = (
  3 * area_from_curvature(K_STARTING)
  + 3 * amount_filled_in_gap(K_OUTER, K_STARTING, K_STARTING)
  + amount_filled_in_gap(K_STARTING, K_STARTING, K_STARTING)
)
frac_not_filled = 1 - (filled / area_from_curvature(K_OUTER))
print('{:.8f}'.format(frac_not_filled))
