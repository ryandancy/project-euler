#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 233:

Let f(N) be the number of points with integer coordinates that are on a circle passing through (0,0), (N,0), (0,N), and
(N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420?
"""

'''
A circle that passes through (0, 0), (N, 0), (0, N), and (N, N) will have its centre at the average of the X and Y
coordinates of each point: (N/2, N/2). Its radius will then be sqrt((N/2 - 0)^2 + (N/2 - 0)^2) = N/sqrt(2) = Nsqrt(2)/2.
The equation of that circle is then (x - N/2)^2 + (y - N/2)^2 = N^2/2.

However, we are concerned merely with the number of integral solutions to this equation. If N is even (and therefore N/2
is an integer), (x - N/2)^2 + (y - N/2)^2 = N^2/2 has the same number of solutions as x^2 + y^2 = N^2/2, since the
lattice points are merely shifted. Similarly, if N is odd (and therefore N/2 is of the form k + 1/2, where k is an
integer), the number of integral solutions is equivalent to that of (x - 1/2)^2 + (y - 1/2)^2 = N^2/2. This equation too
has the same number of integral solutions as x^2 + y^2 = 2N^2, since doubling the radius (by multiplying by 2^2 = 4)
and shifting by (-1/2, -1/2) turns each solution of the form k + 1/2 (with k an integer) into an integer.

Furthermore, in the generic equation x^2 + y^2 = m, let C_1 be the number of divisors of m that equal 1 modulo 4
(the count of d > 0, d|m, d = 1 (mod 4)), and let C_3 be the number of divisors of m that equal 3 modulo 4 (the count of
d > 0, d|m, d = 3 (mod 4)). The number of integer solutions is then 4(C_1 - C_3).

Let us consider the equation x^2 + y^2 = N^2/2. The divisors of N^2/2, modulo 4, will be of the form 4n + k, where k =
0, 1, 2, or 3. Multiplying an integer Q by 2 has the effect that for each divisor d where d|Q, 2Q will have two divisors
d|2Q and 2d|2Q. We shall now prove that multiplying N^2/2 by 2 (to yield N^2) will produce no new divisors of the form
4n + 1 or 4n + 3 (which would affect C_1 and C_3, and thus the number of integer solutions) by multiplying each possible
form of divisor by 2.

If k = 0:
2(4n + 0) = 8n
          = 4(2n)
          = 4m for some integer m = 2n. Thus C_1 and C_3 are unaffected.

If k = 1:
2(4n + 1) = 8n + 2
          = 4(2n) + 2
          = 4m + 2 for some integer m = 2n. Thus C_1 and C_3 are unaffected.

If k = 2:
2(4n + 2) = 8n + 4
          = 4(2n + 1)
          = 4m for some integer m = 2n + 1. Thus C_1 and C_3 are unaffected.

If k = 3:
2(4n + 3) = 8n + 6
          = 8n + 4 + 2
          = 4(2n + 2) + 2
          = 4m + 2 for some integer m = 2n + 2. Thus C_1 and C_3 are unaffected.

Therefore N^2/2 may be multiplied by 2 without affecting the number of integer solutions; x^2 + y^2 = N^2/2 thus has the
same number of integer solutions as x^2 + y^2 = N^2.

Similarly, in x^2 + y^2 = 2N^2, dividing 2N^2 by 2 merely removes the divisors formed by multiplying by 2, and thus does
not affect the number of integer solutions; therefore x^2 + y^2 = 2N^2 has the same number of integer solutions as x^2 +
y^2 = N^2.

The task is now to find all values of N <= 10^11 such that there are 420 integer solutions to x^2 + y^2 = N^2. The
number of integer solutions (lattice points) for N >= 0 is sequence A046109 in the OEIS. There, Orson R. L. Peters has
proven that the number of integer solutions is equal to 4 times the product of (2e_i + 1) for each e_i, where e_i is the
exponent of each prime p_i in the prime factors of N, where p_i = 1 (mod 4). For example, if N = 650 = 2*5^2*13, then
x^2 + y^2 = N^2 has 4(2*2 + 1)(2*1 + 1) = 60 solutions (since 5 = 13 = 1 (mod 4), but 2 = 2 (mod 4)).

To find values of N with 420 integer solutions, we must simply find values of N with prime factors of the form described
above. Since 420/4 = 105, the product of each (2e_i + 1) must be 105. There are 5 distinct ways to write 105 as a
product of integers of the form (2e_i + 1):

105 = 3 * 5 * 7 = (2*1 + 1)(2*2 + 1)(2*3 + 1)
    = 7 * 15    = (2*3 + 1)(2*7 + 1)
    = 3 * 35    = (2*1 + 1)(2*17 + 1)
    = 5 * 21    = (2*2 + 1)(2*10 + 1)
    = 105       = (2*52 + 1)

All permutations of the above must be considered as well; there are therefore 13 possible prime exponent permutations
that must be considered.

Note that multiplying any number with prime factors of the above format by a prime which is not equal to 1 (mod 4) does
not change the number of integer solutions, but does produce a different number. For example, 5^3 * 13^2 * 17 = 359125
and 2 * 5^3 * 13^2 * 17 = 718250 are both valid solutions with 420 lattice points, but are different numbers. Thus all
possible combinations of non-1 mod 4 prime coefficients must also be considered.

This program generates primes and sorts them into "1mod4" and "non_1mod4" lists. It goes through every permutation of
the above exponent combinations. For each one, it goes through each number with that combination of 1mod4 prime factors,
then multiplies that number by each combination of non-1mod4 prime factors to generate each number.

This program takes ~13.5 hours to produce the correct result.
'''

from itertools import count

primes = set()
def gen_primes():
  for n in count(2):
    for prime in primes:
      if n % prime == 0:
        break
    else:
      primes.add(n)
      yield n

primes_1mod4 = []
primes_non_1mod4 = []
primes_generator = gen_primes()

def sort_next_prime():
  next_prime = next(primes_generator)
  if next_prime % 4 == 1:
    primes_1mod4.append(next_prime)
  else:
    primes_non_1mod4.append(next_prime)

def nth_prime_1mod4(n): # zero-indexed
  while n >= len(primes_1mod4):
    sort_next_prime()
  return primes_1mod4[n]

def nth_prime_non_1mod4(n): # also zero-indexed
  while n >= len(primes_non_1mod4):
    sort_next_prime()
  return primes_non_1mod4[n]

LIMIT = 10**11

def total_for_1mod4_combo(base_num):
  # this really should be recursive, but the stack overflows, so this is an iterative solution using a stack
  
  stack = []
  
  highest_non_1mod4_idx = 0
  
  while base_num * nth_prime_non_1mod4(highest_non_1mod4_idx) <= LIMIT:
    stack.append((base_num, highest_non_1mod4_idx, 1))
    highest_non_1mod4_idx += 1
  
  this_total = base_num # adding base_num for the all 0s case
  
  while stack:
    base_num, highest_non_1mod4_idx, start_at = stack.pop()
    highest_non_1mod4_prime = nth_prime_non_1mod4(highest_non_1mod4_idx)
    
    for power in count(start_at):
      composed = base_num * highest_non_1mod4_prime**power
      
      if composed > LIMIT:
        break
      
      if highest_non_1mod4_idx == 0:
        this_total += composed
      else:
        stack.append((composed, highest_non_1mod4_idx - 1, 0))
  
  return this_total

power_configurations = (
  (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1),
  (3, 7), (7, 3),
  (1, 17), (17, 1),
  (2, 10), (10, 2),
  (52,)
)

def total_length_3_combo(p0, p1, p2, n): # return: (total, continue with this combo?)
  this_total = 0
  
  for prime_0_idx in range(n-1):
    for prime_1_idx in range(prime_0_idx + 1, n):
      num = nth_prime_1mod4(prime_0_idx)**p0 * nth_prime_1mod4(prime_1_idx)**p1 * nth_prime_1mod4(n)**p2
      
      if n % 100 == 0 and prime_0_idx == 0 and prime_1_idx == 1:
        print(n, num, '{:.2f}%'.format(num / LIMIT * 100))
      
      if num > LIMIT:
        if prime_0_idx == 0 and prime_1_idx == 1:
          return this_total, False
        else:
          break
      
      this_total += total_for_1mod4_combo(num)
  
  return this_total, True

def total_length_2_combo(p0, p1, n): # return: (total, continue with this combo?)
  this_total = 0
  
  for prime_0_idx in range(n):
    num = nth_prime_1mod4(prime_0_idx)**p0 * nth_prime_1mod4(n)**p1
    
    if num > LIMIT:
      if prime_0_idx == 0:
        return this_total, False
      else:
        break
    
    this_total += total_for_1mod4_combo(num)
  
  return this_total, True

def total_length_1_combo(p, n): # return (total, continue with this combo?)
  num = nth_prime_1mod4(n)**p
  
  if num > LIMIT:
    return 0, False
  else:
    return total_for_1mod4_combo(num), True

if __name__ == '__main__':
  total = 0
  
  for power_config in power_configurations:
    for n in count(len(power_config) - 1):
      num = 1
      
      if len(power_config) == 3:
        p0, p1, p2 = power_config
        this_total, continue_combo = total_length_3_combo(p0, p1, p2, n)
      elif len(power_config) == 2:
        p0, p1 = power_config
        this_total, continue_combo = total_length_2_combo(p0, p1, n)
      else: # len is 1
        this_total, continue_combo = total_length_1_combo(power_config[0], n)
      
      total += this_total
      if not continue_combo:
        break
    
    print('Done power config {}: total = {}'.format(power_config, total))

  print(total)
