#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 93:

By using each of the digits from the set, {1, 2, 3, 4}, exactly once, and making use of the four arithmetic operations
(+, −, *, /) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

8 = (4 * (1 + 3)) / 2
14 = 4 * (3 + 1 / 2)
19 = 4 * (2 + 3) − 1
36 = 3 * 4 * (2 + 1)

Note that concatenations of the digits, like 12 + 34, are not allowed.

Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one different target numbers of which 36 is the maximum,
and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, a < b < c < d, for which the longest set of consecutive positive integers, 1 to n,
can be obtained, giving your answer as a string: abcd.
"""

# Using eval (but it's not arbitrary code so it's fine) and lots of generators and use of itertools
# The numbers, their order, the operators, and the parentheses' locations must be generated
# Runs in ~1.5 minutes

from itertools import combinations, permutations, product, count, takewhile, zip_longest

op_combos = list(product('+-*/', repeat=3))

def gen_parens(start=0, end=4):
  window_len = end - start - 1
  if window_len < 1:
    return set()
  
  yield {(start, end - 1)}
  
  while window_len:
    for s in range(start, end - window_len + 1):
      e = s + window_len
      for window in gen_parens(s, e):
        yield {*window, (start, end - 1)}
    window_len -= 1

paren_combos = list(gen_parens())

def eval_combo(abcd, ops, parens):
  nums = list(map(str, abcd))
  for open_, close in parens:
    nums[open_] = '(' + nums[open_]
    nums[close] += ')'
  expr = ''.join(x for tup in zip_longest(nums, ops, fillvalue='') for x in tup)
  try:
    return eval(expr)
  except ZeroDivisionError:
    return -1

most_consecutive = 0
best_abcd = None

for a, b, c, d in combinations(range(10), 4):
  values = {eval_combo((a0, b0, c0, d0), ops, parens) for a0, b0, c0, d0 in permutations((a, b, c, d), 4)
            for ops in op_combos for parens in paren_combos}
  consecutive = len(list(takewhile(values.__contains__, count(1))))
  if consecutive > most_consecutive:
    most_consecutive = consecutive
    best_abcd = ''.join(map(str, (a, b, c, d)))

print(best_abcd)
