#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 54:

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights
beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then
highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are
compared, and so on.

Consider the following hand dealt to two players:

    Player 1       Player 2      Winner
5H 5C 6S 7S KD  2C 3S 8S 8D TD  Player 2
Pair of Fives   Pair of Eights

The file data/p054_poker.txt contains one-thousand random hands dealt to two players. Each line of the file contains ten
cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can
assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order,
and in each hand there is a clear winner.

How many hands does Player 1 win?
"""

from collections import Counter
from functools import total_ordering

CARD_VALUES = {
  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}
CARD_SUITS = {'H': 0, 'D': 1, 'C': 2, 'S': 3}

@total_ordering
class Card:
  
  def __init__(self, string):
    self.value = CARD_VALUES[string[0]]
    self.suit = CARD_SUITS[string[1]]
  
  def __gt__(self, other):
    return self.value > other.value
  
  def __eq__(self, other):
    return self.value == other.value and self.suit == other.suit
  
  def __str__(self):
    return str((self.value, self.suit))

def rank_hand(hand): # returns list of (ranking, tiebreaker)
  rankings = []
  hand.sort()
  
  values = [card.value for card in hand]
  values_counter = Counter(values)
  
  flush = all(card.suit == hand[0].suit for card in hand)
  straight = all(value == values[i+1] - 1 for i, value in enumerate(values[:-1]))
  
  if flush and values == [10, 11, 12, 13, 14]:
    # royal flush
    rankings.append((10, 0))
  
  if straight and flush:
    # straight flush
    rankings.append((9, values[-1]))
  
  if 4 in values_counter.values():
    # four of a kind
    rankings.append((8, values_counter.most_common()[0][0]))
  
  if set(values_counter.values()) == {3, 2}:
    # full house
    three, two = values_counter.most_common()
    rankings.append((7, three[0] * 100 + two[0]))
  
  if flush:
    # flush
    rankings.append((6, 0)) # delegate to the lower one
  
  if straight:
    # straight
    rankings.append((5, values[-1]))
  
  if 3 in values_counter.values():
    # three of a kind
    rankings.append((4, values_counter.most_common()[0][0]))
  
  if list(values_counter.values()).count(2) == 2:
    # two pairs
    higher, lower = sorted([value for value in set(values) if values_counter[value] == 2], reverse=True)[:2]
    rankings.append((3, higher * 100 + lower))
  
  if 2 in set(values_counter.values()):
    # one pair
    pair_value = next(value for value in values if values_counter[value] == 2)
    rankings.append((2, pair_value))
  
  # high card
  for value in values[::-1]:
    rankings.append((1, value))
  
  return rankings

def first_wins(ranking1, ranking2):
  # trust that they're in order
  for (r1, tie1), (r2, tie2) in zip(ranking1, ranking2):
    if r1 > r2:
      return True
    elif r1 < r2:
      return False
    elif tie1 > tie2:
      return True
    elif tie1 < tie2:
      return False

with open('data/p054_poker.txt') as poker_file:
  hands = poker_file.readlines()

player1_hands = 0

for hand in hands:
  cards = list(map(Card, hand.split()))
  hand1 = cards[:5]
  hand2 = cards[5:]
  
  if first_wins(rank_hand(hand1), rank_hand(hand2)):
    player1_hands += 1

print(player1_hands)
