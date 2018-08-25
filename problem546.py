#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 546:

Define f_k(n) = ∑^n_{i=0} f_k(⌊i/k⌋) where f_k(0) = 1 and ⌊x⌋ denotes the floor function.

For example, f_5(10) = 18, f_7(100) = 1003, and f_2(10^3) = 264830889564.

Find (∑^{10}_{k=2} f_k(10^14)) mod (10^9+7).
"""

"""
It turns out that f_k(n) is equivalent to b_m(n), a function which counts the m-ary partitions of n, i.e. the number of
ways n can be represented as a sum of non-negative powers of m (see sequence A000123 in the OEIS).

Sun and Zhang in https://arxiv.org/abs/1706.07148 give a formula that relates b_m(n) to the base m representation of n:
if (a_j, a_{j-1}, ..., a_1, a_0) is the base m representation of n (i.e. n = sum_{i=0}^j a_i*m^i), then
b_m(n) = sum_{k_j = 0}^a_j sum_{k_{j-1} = 0}^{a_{j-1} + mk_j} ... sum_{k_1 = 0}^{a_1 + mk_2} 1.

When one implements b_m(n) using the above algorithm and memoizes the sum given (idx, mk_x) at each summation, where idx
is the index into the list a (i.e. idx goes from 1 to j), a curious pattern emerges. Given that j is the number of
digits in the base m representation of n, the sequence of memoized sums with idx = j - i (for 0 <= i < j), when sorted,
has an ith difference of m^T(i), where T(i) is the ith triangular number.

This solution exploits this pattern to calculate only i terms for the ith digit. The first term of the sequence with
idx = 1 is a_1 + 1; we then determine enough terms of the ith sequence that the terms of the next sequence (with a
greater degree, and thus requiring more starting terms) may be determined.

At a certain point, however, the "canonical" Sun/Zhang solution with j-fold sums does not have enough terms to form
a polynomial sequence of high degree, and it breaks down. This point is where the degree of the sequence would exceed
the number of terms in the sequence. The number of terms may be modeled by m^(j-i); when this is less than the degree of
the sequence, we switch to simply aggregating sums.

This solution runs in ~0.2 seconds.
"""

MODULUS = 10**9 + 7

def convert_to_base(b, n):
  # Return n converted to base b as a sequence of digits from least to most significant
  converted = []
  while n > 0:
    n, digit = divmod(n, b)
    converted.append(digit)
  return converted

def T(n):
  # nth triangular number
  return n * (n + 1) // 2

def get_range(starts, diff_num, diff, k_limit):
  # Find all differences up to diff_num
  diffs = [starts[:]] # diffs[i] is the list of ith differences
  for i in range(1, diff_num):
    diffs.append([b - a for a, b in zip(diffs[i-1], diffs[i-1][1:])])
  
  # Extend the differences, propagate them down
  to_extend = k_limit - len(starts)
  for i in range(1, to_extend + 1): # if len(starts) == diff_num then len(diffs[diff_num-1]) == 1
    diffs[diff_num - 1].append(diffs[diff_num - 1][i - 1] + diff)
    for level in range(diff_num - 2, -1, -1):
      diffs[level].append(diffs[level][-1] + diffs[level + 1][-1])
  
  return diffs[0]

def f(m, n):
  digits = convert_to_base(m, n) # least to most significant
  starts = [[digits[0] + 1]]
  
  # Evaluate each for addend = 0m, 1m, 2m, ..., im to determine the i+1 starting numbers
  for i in range(1, len(digits)):
    if m**(len(digits) - i) < i:
      break
    
    irange = get_range(starts[i - 1], i, m**T(i), digits[i] + i*m + 1)
    istarts = [sum(irange[:digits[i] + k*m + 1]) for k in range(i + 1)]
    starts.append(istarts)
  
  # At this point there are fewer numbers in the "canonical" method than the constant difference number, so a polynomial
  # sequence no longer applies; this does instead
  for j in range(i, len(digits)):
    starts.append([sum(starts[j - 1][:digits[j] + k*m + 1]) for k in range(i + 1)])
  
  return starts[-1][0]

print(sum(f(i, 10**14) for i in range(2, 11)) % MODULUS)
