#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 144:

In laser physics, a "white cell" is a mirror system that acts as a delay line for the laser beam. The beam enters the
cell, bounces around on the mirrors, and eventually works its way back out.

The specific white cell we will be considering is an ellipse with the equation 4x^2 + y^2 = 100

The section corresponding to −0.01 ≤ x ≤ +0.01 at the top is missing, allowing the light to enter and exit through the
hole.

The light beam in this problem starts at the point (0.0,10.1) just outside the white cell, and the beam first impacts
the mirror at (1.4,-9.6).

Each time the laser beam hits the surface of the ellipse, it follows the usual law of reflection "angle of incidence
equals angle of reflection." That is, both the incident and reflected beams make the same angle with the normal line at
the point of incidence.

The slope m of the tangent line at any point (x,y) of the given ellipse is: m = −4x/y

The normal line is perpendicular to this tangent line at the point of incidence.

How many times does the beam hit the internal surface of the white cell before exiting?
"""

'''
The normal line is perpendicular to the tangent line; its slope is therefore y/4x (the negative reciprocal of -4x/y).

The angle of incidence between the normal (slope m_n) and an incoming ray (slope m_1) can be calculated with the formula

theta = |arctan((m_1 - m_n) / (1 + m_1*m_n))|.

This is based on the trigonometric identity tan(A-B) = (tan A - tan B) / (1 + tan A * tan B) and the fact that slope is
just a tangent. Since the angle of incidence equals the angle of reflection, the angle between the normal and the
incoming ray equals the angle betweeen the normal and the outgoing ray (slope m_2). Adjusting for signs, this gives

(m_1 - m_n) / (1 + m_1*m_n) = (m_n - m_2) / (1 + m_2*m_n),

which may be rearranged to give

m_2 = (m_1*m_n^2 - m_1 + 2*m_n) / (1 + 2*m_1*m_n - m_n^2).

In this way, the slope of the reflection line may be calculated from that of the normal and the incident line.

As well, to find the points of intersection between the ellipse and an arbitrary line, the system
{y = mx + b, 4x^2 + y^2 = 100} must be solved. Doing so yields

x = (-mb +/- 2*sqrt(25m^2 - b^2 + 100)) / (m^2 + 4),

and y may be calculated as mx + b. When performing this calculation, two points are yielded: the point where the laser
beam bounced last and where it will bounce next. However, the previous-bounce point may not be exactly the previous
values of x and y due to floating-point errors; to counteract this, this program calculates the Euclidean distance
between the previous values of x and y and the two intersection points generated and selects the point furthest away
from the previous point.

This program repeatedly calculates the slopes and points of intersection until the point of intersection has y > 0 and
-0.01 < x < 0.01. It runs in approximately 0.1 seconds.
'''

from math import sqrt

initial_x, initial_y = (0, 10.1)
x, y = (1.4, -9.6)

m = (initial_y - y) / (initial_x - x)
b = y - m*x

bounces = 0

while not (y > 0 and -0.01 <= x <= 0.01):
  # compute new slope of line + y-intercept
  m_n = y / (4*x)
  m = (m*m_n*m_n - m + 2*m_n) / (1 + 2*m*m_n - m_n*m_n)
  b = y - m*x
  
  # compute POI
  s = sqrt(25*m*m - b*b + 100)
  mb = m*b
  mm4 = m*m + 4
  
  # Two options for second POI, choose the one that's furthest away from (x, y) to avoid floating-point errors
  nx1 = (2*s - mb) / mm4
  nx2 = (-2*s - mb) / mm4
  ny1 = m*nx1 + b
  ny2 = m*nx2 + b
  
  dist1 = sqrt((nx1 - x)**2 + (ny1 - y)**2)
  dist2 = sqrt((nx2 - x)**2 + (ny2 - y)**2)
  
  if dist1 > dist2:
    x, y = nx1, ny1
  else:
    x, y = nx2, ny2
  
  bounces += 1

print(bounces)
