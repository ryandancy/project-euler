#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 91:

The points P (x1, y1) and Q (x2, y2) are plotted at integer co-ordinates and are joined to the origin, O(0,0), to form
ΔOPQ.

There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between 0
and 2 inclusive; that is, 0 ≤ x1, y1, x2, y2 ≤ 2.

Given that 0 ≤ x1, y1, x2, y2 ≤ 50, how many right triangles can be formed?
"""

"""
It can easily be determined that there exist MAX^2 right-angled triangles (where MAX is the maximum coordinate on the
grid) where the right angle is at the origin; similarly, there are 2*MAX^2 right-angled triangles where the right angle
is at x=0 xor y=0. The difficulty in this problem comes from determining the number of right-angled triangles with
neither x nor y at 0.

Our strategy is for each point (x_1, y_1) with 0 < x_1, y_1 <= MAX to find the number of integer solutions between 0 and
MAX (x, y) that solve the Diophantine equation y = (-x_1/y_1)x + b, where b is the y-intercept (and, it turns out, is
irrelevant for this purpose). If p = x_1 / gcd(x_1, y_1) and q = y_1 / gcd(x_1, y_1) (both integers), the above equation
simplifies to px + qy = qb.

At https://math.stackexchange.com/a/20727, Arturo Magidin has proven that if (x_1, y_1) is a solution to the Diophantine
equation px + qy = n, then subsequent solutions are found through the relation x = x_1 - r*q/gcd(p, q), y = y_1
+ r*p/gcd(p, q) for some integer r. Since we already defined gcd(p, q) = 1, this simplifies to x = x_1 - rq, y = y_1
+ rp.

The question is now how many values of r exist such that 0 <= x, y <= MAX. We may find this by finding the values of r
at which x = 0, x = MAX, y = 0, and y = MAX. These are:

If x = 0, r = x_1 / q. (r is positive)
If x = MAX, r = (x_1 - MAX) / q. (r is negative)
If y = 0, r = -y_1 / q. (r is negative)
If y = MAX, r = (50 - y_1) / q. (r is positive)

Using these, we may find the number of values of r (both negative and positive) for a given (x_1, y_1), which is the
number of right-angled triangles with the right angle at (x_1, y_1) on the grid.

This solution using this runs in ~0.1 seconds.
"""

from math import gcd

MAX = 50

# MAX^2 with right angle at origin, 2*MAX^2 with right angle at x=0 xor y=0
total = 3 * MAX**2

# Right angle not at x=0 or y=0
for x1 in range(1, MAX + 1):
  for y1 in range(1, MAX + 1):
    # Reduce x1, y1 by the gcd so that the coming Diophantine equation is always solvable
    xygcd = gcd(x1, y1)
    p, q = x1 // xygcd, y1 // xygcd
    
    # We now find the number of solutions to the Diophantine equation px + qy = qb, where b is the y-intercept.
    # By Arturo Magidin's excellent math.SE answer at https://math.stackexchange.com/a/20727,
    # if one solution is (x_1, y_1), further solutions are found by x = x_1 - r*q/gcd(p, q), y = y_1 + r*p/gcd(p, q),
    # where r is any integer. Since gcd(p, q) = 1, the relation x = x_1 - r*q, y = y_1 + r*p is used.
    
    # Positive r: y=MAX when r=(MAX-y_1)/p, x=0 when r=x_1/q
    total += int(min((MAX - y1) / p, x1 / q))
    
    # Negative r: y=0 when r=-y_1/p, x=MAX when r=(x_1-MAX)/q
    total += int(-max(-y1 / p, (x1 - MAX) / q))

print(total)
