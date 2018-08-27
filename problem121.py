#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 121:

A bag contains one red disc and one blue disc. In a game of chance a player takes a disc at random and its colour is
noted. After each turn the disc is returned to the bag, an extra red disc is added, and another disc is taken at random.

The player pays £1 to play and wins if they have taken more blue discs than red discs at the end of the game.

If the game is played for four turns, the probability of a player winning is exactly 11/120, and so the maximum prize
fund the banker should allocate for winning in this game would be £10 before they would expect to incur a loss. Note
that any payout will be a whole number of pounds and also includes the original £1 paid to play the game, so in the
example given the player actually wins £9.

Find the maximum prize fund that should be allocated to a single game in which fifteen turns are played.
"""

# At a given round n, the probability of picking a blue disc is 1/(n+1).
# The probability of at least m events out of n happening is the sum of the probabilities of each combination of m or
# greater events happening.
# The maximum prize fund is e/p, where e is the amount the player pays and p is the total probability of winning.
# This solution based on the above runs in ~0.2 seconds.

from itertools import combinations

ROUNDS = 15
CHANCES = [1/n for n in range(2, ROUNDS + 2)]

total_chance = 0

for num_blue in range(ROUNDS//2 + 1, ROUNDS + 1):
  for round_combo in combinations(list(range(ROUNDS)), num_blue):
    this_chance = 1
    for round_ in range(ROUNDS):
      if round_ in round_combo:
        this_chance *= CHANCES[round_]
      else:
        this_chance *= 1 - CHANCES[round_]
    total_chance += this_chance

print(int(1 / total_chance))
