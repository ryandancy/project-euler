#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 81:

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by only moving to the right and
down, is indicated with asterisks and is equal to 2427.

*131  673  234  103  18
*201 *96  *342  965  150
 630  803 *746 *422  111
 537  699  497 *121  956
 805  732  524 *37  *331

Find the minimal path sum, in data/p081_matrix.txt, a 31K text file containing a 80 by 80 matrix, from the top left to
the bottom right by only moving right and down.
"""

# Djikstra's algorithm
# Runs in ~5 seconds

SIZE = 80

with open('data/p081_matrix.txt') as matrix_file:
  # access: matrix[y][x]
  matrix = [list(map(int, line.split(','))) for line in matrix_file.readlines()]

# Process the matrix into a graph from top-left to bottom-right
graph = {}
for y in range(SIZE):
  for x in range(SIZE):
    graph[(x, y)] = set()
    if x + 1 < SIZE:
      graph[(x, y)].add((x + 1, y))
    if y + 1 < SIZE:
      graph[(x, y)].add((x, y + 1))

# Djikstra's algorithm on the graph
INFINITY = 10**100
distances = {(x, y): INFINITY for x in range(SIZE) for y in range(SIZE)}
distances[(0, 0)] = matrix[0][0]

unvisited = {(x, y) for x in range(SIZE) for y in range(SIZE)}

while unvisited:
  current = min(unvisited, key=lambda xy: distances[xy])
  unvisited.remove(current)
  
  for nx, ny in graph[current]:
    tentative = distances[current] + matrix[ny][nx]
    if tentative < distances[(nx, ny)]:
      distances[(nx, ny)] = tentative

print(distances[(SIZE - 1, SIZE - 1)])
