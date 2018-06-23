#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 18:

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top
to bottom is 23.

   3
  7 4
 2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom of the triangle below:

              75
             95 64
            17 47 82
           18 35 87 10
          20 04 82 47 65
         19 01 23 75 03 34
        88 02 77 73 07 63 67
       99 65 04 28 06 16 70 92
      41 41 26 56 83 40 80 70 33
     41 48 72 33 47 32 37 16 94 29
    53 71 44 65 25 43 91 52 97 51 14
   70 11 33 28 77 73 17 78 39 68 17 57
  91 71 52 38 17 14 91 43 58 50 27 29 48
 63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
"""

# Use something like Djiksta's algorithm, but searching for the highest-value path

from collections import defaultdict

# Build a graph of the triangle
# Format is id: ((to_id1, weight1), (to_id2, weight2))

triangle_list = [list(map(int, row.split(' '))) for row in '''\
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23'''.split('\n')]

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
