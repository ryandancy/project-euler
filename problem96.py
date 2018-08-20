#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 96:

Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit
must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares.
The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row,
column, and 3 by 3 box contains each of the digits 1 to 9.

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to
employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The
complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be
solved by straight forward direct deduction.

The 6K text file, data/p096_sudoku.txt, contains fifty different Su Doku puzzles ranging in difficulty, but all with
unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for
example, 483 is the 3-digit number found in the top left corner of the solution grid above.
"""

from itertools import combinations

# STRATEGIES

def sole_candidate(puzzle):
  for x, y in Puzzle.ALL_COORDS:
    candidates = puzzle.candidates(x, y)
    if len(candidates) == 1:
      puzzle.set_number(x, y, candidates[0])
      return True
  return False

def check_for_unique_candidates(puzzle, all_coords, all_candidates):
  for num in range(1, 10):
    found_one = False
    fx, fy = None, None
    
    for (x, y), candidates in zip(all_coords, all_candidates):
      if num not in candidates:
        continue
      
      if found_one:
        found_one = False
        break
      else:
        found_one = True
        fx, fy = x, y
    
    if found_one:
      puzzle.set_number(fx, fy, num)
      print('unique candidate at', fx, ',', fy, 'setting to', num, '; coords:', all_coords)
      return True
  
  return False

def unique_candidate(puzzle):
  # check blocks
  for block_start_x in range(0, 7, 3):
    for block_start_y in range(0, 7, 3):
      block_coords = puzzle.block_coords(block_start_x, block_start_y)
      block_candidates = [puzzle.candidates(x, y) for x, y in block_coords]
      
      if check_for_unique_candidates(puzzle, block_coords, block_candidates):
        return True
  
  # check columns
  for col in range(9):
    coords = puzzle.column_coords(col)
    candidates = [puzzle.candidates(x, y) for x, y in coords]
    
    if check_for_unique_candidates(puzzle, coords, candidates):
      return True
  
  # check rows
  for row in range(9):
    coords = puzzle.row_coords(row)
    candidates = [puzzle.candidates(x, y) for x, y in coords]
    
    if check_for_unique_candidates(puzzle, coords, candidates):
      return True
  
  return False

def block_column_row_interaction(puzzle):
  for block_start_x in range(0, 7, 3):
    for block_start_y in range(0, 7, 3):
      coords = puzzle.block_coords(block_start_x, block_start_y)
      candidates = [puzzle.candidates(x, y) for x, y in coords]
      
      for num in range(1, 10):
        # find the coords with this candidate
        coords_for_num = [(x, y) for i, (x, y) in enumerate(coords) if num in candidates[i]]
        changed_something = False
        
        # are they all in one column (same x)?
        if len(set(x for x, y in coords_for_num)) == 1:
          # remove this candidate for all others in this column
          col_num = coords_for_num[0][0]
          
          print('found pointing pair column:', coords_for_num)
          
          for x1, y1 in filter(lambda xy: xy[0] < block_start_x or xy[0] >= block_start_x + 3,
              puzzle.column_coords(col_num)):
            if puzzle.remove_candidate(x1, y1, num):
              print('removed', num, 'from', x1, ',', y1, 'caused by', coords_for_num)
              changed_something = True
          
          if changed_something:
            return True
        
        # are they all in one row (same y)?
        if len(set(y for x, y in coords_for_num)) == 1:
          # remove this candidate for all others in this row
          row_num = coords_for_num[0][1]
          
          print('found pointing pair row:', coords_for_num)
          
          for x1, y1 in filter(lambda xy: xy[1] < block_start_y or xy[1] >= block_start_y + 3,
              puzzle.row_coords(row_num)):
            if puzzle.remove_candidate(x1, y1, num):
              print('removed', num, 'from', x1, ',', y1, 'caused by', coords_for_num)
              changed_something = True
          
          if changed_something:
            return True
  
  return False

def block_block_interaction(puzzle):
  # TODO. I don't feel like doing this right now.
  return False

def check_for_naked_subset(puzzle, coords, candidates):
  # find a subset that's either fully in a candidate or out and 'naked' in exactly its length
  for cands in candidates:
    if len(cands) > 1 and candidates.count(cands) == len(cands):
      # is there any case where cands is "partially" in a list of candidates?
      to_remove = []
      abort = False
      
      for (x, y), cands2 in zip(coords, candidates):
        if set(cands2) > set(cands):
          # cands2 is a superset of cands
          to_remove.append((x, y))
        elif set(cands2) & set(cands):
          # cands2 is partially in cands, invalidating this
          abort = True
          break
      
      if abort:
        continue
      
      # do our duty
      changed_something = False
      for x, y in to_remove:
        if puzzle.remove_candidate(x, y):
          changed_something = True
      if changed_something:
        return True
  
  return False

def naked_subset(puzzle):
  # blocks
  for block_start_x in range(0, 7, 3):
    for block_start_y in range(0, 7, 3):
      coords = puzzle.block_coords(block_start_x, block_start_y)
      candidates = [puzzle.candidates(x, y) for x, y in coords]
      
      if check_for_naked_subset(puzzle, coords, candidates):
        return True
  
  # columns
  for col in range(9):
    coords = puzzle.column_coords(col)
    candidates = [puzzle.candidates(x, y) for x, y in coords]
    
    if check_for_naked_subset(puzzle, coords, candidates):
      return True
  
  # rows
  for row in range(9):
    coords = puzzle.row_coords(row)
    candidates = [puzzle.candidates(x, y) for x, y in coords]
    
    if check_for_naked_subset(puzzle, coords, candidates):
      return True
  
  return False

class Puzzle:
  
  # All strategies are functions that take this Puzzle, modify it, and return True for success (placed numbers/removed
  # candidates) or False for failure (did not place numbers/remove candidates)
  STRATEGIES = [
    sole_candidate,
    unique_candidate,
    block_column_row_interaction,
    block_block_interaction,
    naked_subset,
  ]
  
  ALL_COORDS = [(x, y) for x in range(9) for y in range(9)]
  
  def __init__(self, lines):
    self.numbers_grid = [[0 for _ in range(9)] for _ in range(9)]
    self.candidates_grid = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    
    numbers = [list(map(int, line[:-1])) for line in lines]
    
    # to eliminate candidates
    for y, row in enumerate(numbers):
      for x, num in enumerate(row):
        if num != 0:
          self.set_number(x, y, num)
  
  def number(self, x, y):
    return self.numbers_grid[y][x]
  
  def candidates(self, x, y):
    return self.candidates_grid[y][x]
  
  def block_coords(self, x, y):
    return [(dx, dy) for dx in range(x-x%3, x-x%3+3) for dy in range(y-y%3, y-y%3+3)]
  
  def block_numbers(self, x, y):
    return [x for y in self.numbers_grid[y-y%3:y-y%3+3][x-x%3:x-x%3+3] for x in y]
  
  def column_coords(self, x):
    return [(x, y) for y in range(9)]
  
  def column_numbers(self, x):
    return [row[x] for row in self.numbers_grid]
  
  def row_coords(self, y):
    return [(x, y) for x in range(9)]
  
  def row_numbers(self, y):
    return self.numbers_grid[y]
  
  def all_affecting_coords(self, x, y):
    return list(set(self.block_coords(x, y) + self.column_coords(x) + self.row_coords(y)) - {(x, y)})
  
  def set_number(self, x, y, number):
    self.numbers_grid[y][x] = number
    
    # remove all candidates from this number
    self.candidates_grid[y][x] = []
    
    # remove that number from all candidates in its block/row/column
    for x1, y1 in self.all_affecting_coords(x, y):
      self.remove_candidate(x1, y1, number)
  
  def remove_candidate(self, x, y, candidate): # return: True if it removed a candidate, False otherwise
    if candidate in self.candidates_grid[y][x]:
      self.candidates_grid[y][x].remove(candidate)
      return True
    return False
  
  def is_empty(self, x, y):
    return self.numbers_grid[y][x] == 0
  
  def is_solved(self):
    return not any(self.is_empty(x, y) for x, y in Puzzle.ALL_COORDS)
  
  def solve(self):
    while not self.is_solved():
      if not self.try_solve():
        raise ValueError('Could not solve puzzle, dump:\n' + str(self))
  
  def try_solve(self):
    for i, strategy in enumerate(Puzzle.STRATEGIES):
      if strategy(self):
        # the strategy succeeded in doing something - loop back in solve()
        print('strategy {} succeeded'.format(i))
        return True
    return False
  
  def __str__(self):
    return 'Numbers:\n{}\n\nCandidates:\n{}'.format(self.numbers_str(), self.candidates_str())
  
  def numbers_str(self):
    return '\n'.join(' '.join(map(str, row)) for row in self.numbers_grid)
  
  def candidates_str(self):
    pad = max(map(len, map(str, [x for row in self.candidates_grid for x in row])))
    return '\n'.join('  '.join(map(lambda s: s + ' '*(pad-len(s)), map(str, row))) for row in self.candidates_grid)

def main():
  sudoku_lines = []
  
  with open('data/p096_sudoku.txt', 'r') as sudokus:
    while True:
      # the throwaway "Grid X" line - if blank, we've reached the end of the file
      if not sudokus.readline():
        break
      
      sudoku_lines.append([sudokus.readline() for _ in range(9)])
  
  total = 0
  
  for i, lines in enumerate(sudoku_lines):
    puzzle = Puzzle(lines)
    puzzle.solve()
    
    print('Solved puzzle {}:\n{}'.format(i+1, puzzle.numbers_str()))
    
    top_left_number = 100*puzzle.number(0, 0) + 10*puzzle.number(1, 0) + puzzle.number(2, 0)
    total += top_left_number
    
    print('New total: {}'.format(total))
  
  print(total)

if __name__ == '__main__':
  main()
