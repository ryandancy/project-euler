#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 82:

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and finishing in any cell in
the right column, and only moving up, down, and right, is indicated in red and bold; the sum is equal to 994.

 131  673 *234 *103 *18
*201 *96  *342  965  150
 630  803  746  422  111
 537  699  497  121  956
 805  732  524  37   331

Find the minimal path sum, in data/p082_matrix.txt, a 31K text file containing a 80 by 80 matrix, from the left column
to the right column.
"""

# Again, Djikstra's algorithm
# Runs in ~5 seconds

SIZE = 80

with open('data/p082_matrix.txt') as matrix_file:
  # access: matrix[y][x]
  matrix = [list(map(int, line.split(','))) for line in matrix_file.readlines()]

# Process the matrix into a graph from left to right
graph = {}
for y in range(SIZE):
  for x in range(SIZE):
    graph[(x, y)] = set()
    if y - 1 >= 0:
      graph[(x, y)].add((x, y - 1))
    if x + 1 < SIZE:
      graph[(x, y)].add((x + 1, y))
    if y + 1 < SIZE:
      graph[(x, y)].add((x, y + 1))

# Djikstra's algorithm from each cell on the left
INFINITY = 10**100
distances = {(x, y): INFINITY for x in range(SIZE) for y in range(SIZE)}
for y in range(SIZE):
  distances[(0, y)] = matrix[y][0]

unvisited = {(x, y) for x in range(SIZE) for y in range(SIZE)}

while unvisited:
  current = min(unvisited, key=lambda xy: distances[xy])
  unvisited.remove(current)
  
  for nx, ny in graph[current]:
    tentative = distances[current] + matrix[ny][nx]
    if tentative < distances[(nx, ny)]:
      distances[(nx, ny)] = tentative

# Minimum distance on the right side
print(min(distances[(SIZE - 1, y)] for y in range(SIZE)))
