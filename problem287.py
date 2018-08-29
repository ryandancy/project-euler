#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 287:

The quadtree encoding allows us to describe a 2^N×2^N black and white image as a sequence of bits (0 and 1). Those
sequences are to be read from left to right like this:

* the first bit deals with the complete 2^N×2^N region;
* "0" denotes a split: 
  the current 2^n×2^n region is divided into 4 sub-regions of dimension 2^(n-1)×2^(n-1),
  the next bits contains the description of the top left, top right, bottom left and bottom right sub-regions - in that
  order;
* "10" indicates that the current region contains only black pixels;
* "11" indicates that the current region contains only white pixels.

Consider the following 4×4 image (colored marks denote places where a split can occur):
https://projecteuler.net/project/images/p287_quadtree.gif

This image can be described by several sequences, for example: "001010101001011111011010101010", of length 30, or
"0100101111101110", of length 16, which is the minimal sequence for this image.

For a positive integer N, define D_N as the 2^N×2^N image with the following coloring scheme:

* the pixel with coordinates x = 0, y = 0 corresponds to the bottom left pixel,
* if (x - 2^(N-1))^2 + (y - 2^(N-1))^2 ≤ 2^(2N-2) then the pixel is black,
* otherwise the pixel is white.

What is the length of the minimal sequence describing D_24?
"""

"""
D_N forms a centred circle in the middle of the grid. Because of this it suffices to check the corner of a square
closest to the centre and the corner furthest away from the centre to determine the makeup of the entire square.

As well, (x-2^(N-1))^2 + (y-2^(N-1))^2 <= 2^(2N-2) simplifies to 2^N(x + y) - x^2 - y^2 >= 2^(2N-2).

Our strategy is to iteratively select a square in each quadrant (defined by the precision value, where the length of
the side of the square is 2**precision, and the starting x and y values, where the square starts at
(startx*2**precision, starty*2**precision)). We then calculate the relevant corner cells to determine the corner cells;
if they give a makeup of the square as a whole, we add 2 to the total; if the square has both black and white cells as
indicated by the corners, we add 9 to the total if the precision is 1 (as the square will have 4 individual cells, each
taking up 2, plus 1 for the 0 to split), or otherwise add 1 to the total and add the four quadrants of the square to the
queue of squares. We do this for all 4 quadrants, then add 1 for the initial "0".

This solution runs in approximately 3 minutes 20 seconds.
"""

N = 24

LENGTH = 2**N
HALF_LENGTH = 2**(N-1)
THRESHOLD = 2**(2*N - 2)

def quadrant_length(add_half_x, add_half_y, bottom_left_top_right, first_short_circuit_value):
  total = 0
  
  second_short_circuit_value = not first_short_circuit_value
  
  queue = [(N - 1, 0, 0)]
  while queue:
    precision, startx, starty = queue.pop()
    
    size = 2**precision
    
    # bottom of square
    y1 = starty*size + (add_half_y * HALF_LENGTH)
    
    if bottom_left_top_right:
      # left of square
      x1 = startx*size + (add_half_x * HALF_LENGTH)
    else:
      # right of square
      x1 = (startx + 1)*size + (add_half_x * HALF_LENGTH) - 1
    
    # This isn't a function call to improve efficiency
    cell1 = (LENGTH*(x1 + y1) - x1*x1 - y1*y1 >= THRESHOLD)
    
    if cell1 == first_short_circuit_value:
      # it's a solid colour
      total += 2
    else:
      # top of square
      y2 = y1 + size - 1
      
      if bottom_left_top_right:
        # right of square
        x2 = x1 + size - 1
      else:
        # left of square
        x2 = x1 - size + 1
      
      cell2 = (LENGTH*(x2 + y2) - x2*x2 - y2*y2 >= THRESHOLD)
      
      if cell2 == second_short_circuit_value:
        # it's the other solid colour
        total += 2
      elif precision == 1:
        # 4 individual cells + the 1 to split
        total += 9
      else:
        # it's mixed - split and add the quarters to the queue
        total += 1
        
        new_precision = precision - 1
        start_x_base, start_y_base = 2*startx, 2*starty
        queue += [
          (new_precision, start_x_base, start_y_base),
          (new_precision, start_x_base + 1, start_y_base),
          (new_precision, start_x_base, start_y_base + 1),
          (new_precision, start_x_base + 1, start_y_base + 1),
        ]
  
  return total

print(
  quadrant_length(True, True, True, False)     # quadrant 1
  + quadrant_length(False, True, False, False) # quadrant 2
  + quadrant_length(False, False, True, True)  # quadrant 3
  + quadrant_length(True, False, False, True)  # quadrant 4
  + 1 # the "0" at the beginning to split
)
