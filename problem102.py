#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Three distinct points are plotted at random on a Cartesian plane, for which -1000 ≤ x, y ≤ 1000, such that a triangle is
formed.

Consider the following two triangles:

A(-340,495), B(-153,-910), C(835,-947)

X(-175,41), Y(-421,-714), Z(574,-645)

It can be verified that triangle ABC contains the origin, whereas triangle XYZ does not.

Using data/p102_triangles.txt, a 27K text file containing the co-ordinates of one thousand "random" triangles, find the
number of triangles for which the interior contains the origin.
"""

# Calculates the barycentric coordinates of the origin in each triangle, then checks that they aren't negative
# (with thanks to https://stackoverflow.com/a/14382692)
# Runs in ~0.1 seconds

from itertools import starmap

def contains_origin(x0, y0, x1, y1, x2, y2):
  # barycentric coordinates with x=0, y=0
  area = 0.5*(-y1*x2 + y0*(-x1+x2) + x0*(y1 - y2) + x1*y2)
  s = 1/(2*area)*(y0*x2 - x0*y2)
  t = 1/(2*area)*(x0*y1 - y0*x1)
  return s > 0 and t > 0 and 1 - s - t > 0

with open('data/p102_triangles.txt') as file_:
  data = [tuple(map(int, line.split(','))) for line in file_]

print(sum(starmap(contains_origin, data)))
