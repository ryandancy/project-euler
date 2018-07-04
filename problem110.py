#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 110:

In the following equation x, y, and n are positive integers.

1/x + 1/y = 1/n

It can be verified that when n = 1260 there are 113 distinct solutions and this is the least value of n for which the
total number of distinct solutions exceeds one hundred.

What is the least value of n for which the number of distinct solutions exceeds four million?
"""

'''
This solution builds on the one used for problem 108, but is far faster.

As explained in the solution to problem 108, the Diophantine equation 1/x + 1/y = 1/n may be rearranged as such:

1/x + 1/y = 1/n
(x + y)/xy = 1/n
xy = nx + ny
x(y - n) = ny
x = ny/(y - n)

Note that a solution for a given positive integer n exists when both x and y are positive integers; i.e., y - n divides
ny. Also note that for any solution y = p and x = ny(y - p), there is an equivalent solution x = p and y = nx(x - p), as
the equation could just have easily been rearranged for y. However, these solutions are not distinct; as there is,
however, a solution where x = y = 2n, the number of distinct solutions is (m + 1)/2, where m is the total number of
solutions.

It can be seen that the first distinct solution is of the form y = n + 1 (giving x = nx + n), and the last is of the
form x = y = 2n. In fact, each distinct solution is of the form y = n + a, where a is a positive integer between 1
and n inclusive. We may substitute y = n + a into the above equation to solve for x:

x = n(n + a)/(n + a - n)
  = (n^2 + na)/a
  = n^2/a + n

If x is an integer (i.e. there is a solution for y = n + a), it is clear that n^2/a must be an integer - a must divide
n^2. In fact, the number of distinct solutions for a given n must be equal to the values of a that divide n^2, or the
number of divisors of n^2 from 1 to n inclusive. However, each divisor b from 1 to n-1 inclusive has a 'counterpart'
divisor n^2/b, so the number of distinct solutions for a given n is equal to (m+1)/2, where m is the total number of
divisors of n^2.

Let N be the minimum number of solutions required; in this case, N = 4000000. If m is again the total number of divisors
of n^2, then n has the minimum number of solutions if:

(m+1)/2 > N
m > 2N - 1

However, since m is an integer, this may be simplified to m >= 2N.

According http://primes.utm.edu/glossary/xpage/tau.html, the total number of divisors of an integer is equal to the
product of the exponents in its prime factors, each plus one. For example, 24 = 2^3 * 3^1, so 24 has (3+1)(1+1) = 8
divisors.

Consider that n = P_1^{k_1} + P_2^{k_2} + ... + P_n^{k_n} where P_n is the nth prime number and k_1 through k_n are some
integer exponents. Then n^2 = (P_1^{k_1} + P_2^{k_2} + ... + P_n^{k_n})^2 = P_1^{2k_1} + P_2^{2k_2} + ... + P_n^{2k_n}.
The total number of divisors of n^2 is then (2k_1 + 1) * (2k_2 + 1) * ... * (2k_n + 1). Thus, there are over N solutions
for a given n when the prime factors of n are k_1, k_2, ..., k_n such that (2k_1 + 1) * (2k_2 + 1) * ... * (2k_n + 1)
>= 2N.

Also, note that if k_2 through k_n are known, the minimum k_1 for a given value of N can be easily calculated:

Let q = (2k_2 + 1) * (2k_3 + 1) * ... * (2k_n + 1).
q(2k_1 + 1) >= 2N
2qk_1 + q >= 2N
2qk_1 >= 2N - q
k_1 >= (2N - q)/2q
k_1 = ceil((2N - q)/2q)

This solution uses this in order to quickly calculate the lowest n that satisfies the constraints. The algorithm finds
the minimum value of n using only the first n_p primes, increasing n_p until the minimum value of n increases (at which
point the previous value of n is the lowest total). It finds the minimum value of n for a given number of primes by
incrementing exponent on the most significant prime and recursing until the minimum value of n begins to increase, at
which point the previous value of n is the lowest and is returned. As well, in order to avoid hanging the program by
calculating enormous powers such as 2^1000000, no exponent over a limit (currently 5000) is evaluated and adjustments
are made to avoid evaluating such enormous powers.

This algorithm finds the minimum value of n for N = 4000000 in just over 2 seconds.
'''

from itertools import count, product
from functools import reduce
import math
import operator

NUM_SOLUTIONS = 4000000
GTE = NUM_SOLUTIONS * 2 # the number everything has to be greater than or equal to; twice the number of solutions
EXPONENT_LIMIT = 5000 # the limit of exponents we'll actually calculate, over that we just compare the exponents

def gen_primes():
  primes = set()
  for n in count(2):
    if all(n % prime for prime in primes):
      yield n
      primes.add(n)

def get_min_k_1(k): # param: k_2 to k_n
  x = reduce(operator.mul, map(lambda k_n: 2*k_n + 1, k))
  return math.ceil((GTE - x) / (2 * x))

def prime_factors_to_int(primes, k):
  return reduce(operator.mul, (p_n**k_n for p_n, k_n in zip(primes, k)))

def k_less_than(primes, k1, k2):
  if k1 == math.inf:
    return False
  if k2 == math.inf:
    return True
  
  # they're lists of exponents; avoid calculating greater than EXPONENT_LIMIT
  if any(k2_n > EXPONENT_LIMIT for k2_n in k2):
    return True
  if any(k1_n > EXPONENT_LIMIT for k1_n in k1):
    return False
  
  return prime_factors_to_int(primes, k1) < prime_factors_to_int(primes, k2)

def find_min(primes, num_primes, k=[]):
  if num_primes == 1:
    return [get_min_k_1(k)]
  
  num_last = 1
  lowest = math.inf
  new = find_min(primes, num_primes - 1, k + [num_last]) + [num_last]
  
  while k_less_than(primes, new, lowest):
    num_last += 1
    lowest = new
    new = find_min(primes, num_primes - 1, k + [num_last]) + [num_last]
  
  return lowest

if __name__ == '__main__':
  num_primes = 2
  prime_gen = gen_primes()
  primes = [next(prime_gen), next(prime_gen)]
  
  lowest_overall = math.inf
  lowest = find_min(primes, num_primes)
  
  while k_less_than(primes, lowest, lowest_overall):
    print('Testing using {} primes, lowest found = {}, lowest overall = {}'.format(num_primes, lowest, lowest_overall))
    
    # Optimize P_1^{k_1} * P_2^{k_2} * ... * P_n^{k_n} where (2k_1 + 1)(2k_2 + 1)...(2k_n + 1) >= 8000000
    num_primes += 1
    primes.append(next(prime_gen))
    
    lowest_overall = lowest
    lowest = find_min(primes, num_primes)
  
  print('Total lowest found:', lowest_overall)
  print('Lowest number:', prime_factors_to_int(primes, lowest_overall))
