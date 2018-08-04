#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 84:

In the game, Monopoly, the standard board is set up in the following way:

GO  A1  CC1 A2  T1  R1  B1  CH1 B2  B3  JAIL
H2                                      C1
T2                                      U1
H1                                      C2
CH3                                     C3
R4                                      R2
G3                                      D1
CC3                                     CC2
G2                                      D2
G1                                      D3
G2J F3  U2  F2  F1  R3  E3  E2  CH2 E1  FP

A player starts on the GO square and adds the scores on two 6-sided dice to determine the number of squares they advance
in a clockwise direction. Without any further rules we would expect to visit each square with equal probability: 2.5%.
However, landing on G2J (Go To Jail), CC (community chest), and CH (chance) changes this distribution.

In addition to G2J, and one card from each of CC and CH, that orders the player to go directly to jail, if a player
rolls three consecutive doubles, they do not advance the result of their 3rd roll. Instead they proceed directly to
jail.

At the beginning of the game, the CC and CH cards are shuffled. When a player lands on CC or CH they take a card from
the top of the respective pile and, after following the instructions, it is returned to the bottom of the pile. There
are sixteen cards in each pile, but for the purpose of this problem we are only concerned with cards that order a
movement; any instruction not concerned with movement will be ignored and the player will remain on the CC/CH square.

Community Chest (2/16 cards):
  Advance to GO
  Go to JAIL
Chance (10/16 cards):
  Advance to GO
  Go to JAIL
  Go to C1
  Go to E3
  Go to H2
  Go to R1
  Go to next R (railway company)
  Go to next R
  Go to next U (utility company)
  Go back 3 squares.

The heart of this problem concerns the likelihood of visiting a particular square. That is, the probability of finishing
at that square after a roll. For this reason it should be clear that, with the exception of G2J for which the
probability of finishing on it is zero, the CH squares will have the lowest probabilities, as 5/8 request a movement to
another square, and it is the final square that the player finishes at on each roll that we are interested in. We shall
make no distinction between "Just Visiting" and being sent to JAIL, and we shall also ignore the rule about requiring a
double to "get out of jail", assuming that they pay to get out on their next turn.

By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate these two-digit numbers to
produce strings that correspond with sets of squares.

Statistically it can be shown that the three most popular squares, in order, are JAIL (6.24%) = Square 10, E3 (3.18%) =
Square 24, and GO (3.09%) = Square 00. So these three most popular squares can be listed with the six-digit modal
string: 102400.

If, instead of using two 6-sided dice, two 4-sided dice are used, find the six-digit modal string.
"""

from collections import Counter
from itertools import product
from fractions import Fraction

ONE_SIXTEENTH = Fraction(1, 16)

GO = 0
JAIL = 10
G2J = 30

COMMUNITY_CHESTS = (2, 17, 33)
CHANCE = (7, 22, 36)

RAILWAYS = (5, 15, 25, 35)
UTILITIES = (12, 28)

NUM_DICE = 2
DICE_SIDES = 6

ITERATIONS = 100

total_rolls = DICE_SIDES ** NUM_DICE
dice_chances = {
  roll: Fraction(total, total_rolls)
  for roll, total in Counter(map(sum, product(range(1, DICE_SIDES + 1), repeat=NUM_DICE))).items()
}

def roll(square):
  result = {}
  for roll, frac in dice_chances.items():
    chances = evaluate((roll + square) % 40)
    for sq, val in chances.items():
      adjusted = frac * val
      if sq in result:
        result[sq] += adjusted
      else:
        result[sq] = adjusted
  return result

def next_square(square, square_list):
  return min(square_list, key=lambda s2: (s2 - square) % 40)

def community_chest(square):
  return {
    square: Fraction(5, 8),
    GO: ONE_SIXTEENTH,
    JAIL: ONE_SIXTEENTH,
  }

def chance(square):
  result = {
    square: Fraction(3, 8),
    GO: ONE_SIXTEENTH,
    JAIL: ONE_SIXTEENTH,
    11: ONE_SIXTEENTH, # C1
    24: ONE_SIXTEENTH, # E3
    39: ONE_SIXTEENTH, # H2
    next_square(square, UTILITIES): ONE_SIXTEENTH,
  }
  
  if square == 36:
    # Back 3 is a community chest - evaluate it
    for sq, val in evaluate(square - 3).items():
      adjusted = val * ONE_SIXTEENTH
      try:
        result[sq] += adjusted
      except KeyError:
        result[sq] = adjusted
    
    # R1 is the next railway
    result[5] = Fraction(3, 16)
  else:
    # Back 3 isn't anything special
    result[(square - 3) % 40] = ONE_SIXTEENTH
    
    # R1 isn't the next railway
    result[5] = ONE_SIXTEENTH
    result[next_square(square, RAILWAYS)] = Fraction(1, 8)
  
  return result

def evaluate(square):
  if square in CHANCE:
    return chance(square)
  elif square in COMMUNITY_CHESTS:
    return community_chest(square)
  elif square == G2J:
    return {JAIL: Fraction(1, 1)}
  else:
    return {square: Fraction(1, 1)}

square_chances = list(map(roll, range(40)))

# Calculate total chances as a weighted average of the square chances, repeat with average chances as weightings

chances = [Fraction(1, 40)] * 40

# Issue: percents add to less than 100% because not every square can be reached from every other square
for _ in range(ITERATIONS):
  chances = [
    sum(
      chances[j] * sqch[i]
      for j, sqch in enumerate(square_chances)
      if i in sqch
    )
    for i in range(40)
  ]
  #print('After {} iterations, chances = {}'.format(_, chances))

# Find highest 3
highest0 = max(range(40), key=lambda i: chances[i])
highest1 = max(set(range(40)) - {highest0}, key=lambda i: chances[i])
highest2 = max(set(range(40)) - {highest0, highest1}, key=lambda i: chances[i])
print(str(highest0) + str(highest1) + str(highest2))

print('Chances:')
for i, chance in enumerate(chances):
  print('{}: {}'.format(i, chance.numerator / chance.denominator))
