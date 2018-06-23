#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 67:

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top
to bottom is 23.

3
7 4
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in data/p067_triangle.txt, a 15K text file containing a triangle with
one-hundred rows.
"""

# This is exactly the same as problem 18's algorithm
# Use something like Djiksta's algorithm, but searching for the highest-value path

from collections import defaultdict

# Build a graph of the triangle
# Format is id: ((to_id1, weight1), (to_id2, weight2))

with open('data/p067_triangle.txt') as tri:
  triangle_list = [list(map(int, row.split(' '))) for row in tri.readlines()]

graph = {}
current_id = 0
for row_num, row in enumerate(triangle_list[:-1]):
  for i, value in enumerate(row):
    to_id = current_id + len(row)
    graph[current_id] = ((to_id, triangle_list[row_num + 1][i]), (to_id + 1, triangle_list[row_num + 1][i + 1]))
    current_id += 1

distances = defaultdict(lambda: 0)
distances[0] = triangle_list[0][0]
current = 0

row_num_to_visit = 0
row_to_visit = {0}
next_row_to_visit = set()

while True:
  if not row_to_visit:
    row_num_to_visit += 1
    if row_num_to_visit == len(triangle_list) - 1:
      # don't visit the last row
      break
    row_to_visit = next_row_to_visit
    next_row_to_visit = set()
  current = max(row_to_visit, key=lambda key: distances[key])
  row_to_visit.remove(current)
  
  neighbours = graph[current]
  current_dist = distances[current]
  
  for neighbour_id, neighbour_weight in neighbours:
    new_dist = current_dist + neighbour_weight
    if new_dist > distances[neighbour_id]:
      distances[neighbour_id] = current_dist + neighbour_weight
    next_row_to_visit.add(neighbour_id)

print(max(distances.values()))
