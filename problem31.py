#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 31:

In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).

It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?
"""

# Dynamic programming: we recurse and calculate the number of ways for each amount and coin combination both using and
# not using the highest-value coin, memoizing on the total amount and types of coins.
# This solution finds the correct solution in ~80ms, much better than the 4-hour runtime of the previous iteration

all_coins = (200, 100, 50, 20, 10, 5, 2, 1)

memoized = {}

def ways(amount, coins=all_coins):
  if (amount, coins) in memoized:
    return memoized[amount, coins]
  if amount == 0 or not coins:
    return 0
  
  # Get the highest-value coin not greater than the amount, clearing too-high-value coins
  coin = coins[0]
  while coin > amount:
    coins = coins[1:]
    coin = coins[0]
  
  result = 0
  if coin == amount:
    # The coin on its own is one way
    result += 1
  else:
    # Find ways using the coin
    result += ways(amount - coin, coins=coins)
  
  # Find ways not using the coin
  result += ways(amount, coins=coins[1:])
  
  memoized[amount, coins] = result
  return memoized[amount, coins]

print(ways(200))
