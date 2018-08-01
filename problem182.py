#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 182:

The RSA encryption is based on the following procedure:

Generate two distinct primes p and q.
Compute n=pq and φ=(p-1)(q-1).
Find an integer e, 1<e<φ, such that gcd(e,φ)=1.

A message in this system is a number in the interval [0,n-1].
A text to be encrypted is then somehow converted to messages (numbers in the interval [0,n-1]).
To encrypt the text, for each message, m, c=me mod n is calculated.

To decrypt the text, the following procedure is needed: calculate d such that ed=1 mod φ, then for each encrypted
message, c, calculate m=cd mod n.

There exist values of e and m such that me mod n=m.
We call messages m for which me mod n=m unconcealed messages.

An issue when choosing e is that there should not be too many unconcealed messages. 
For instance, let p=19 and q=37.
Then n=19*37=703 and φ=18*36=648.
If we choose e=181, then, although gcd(181,648)=1 it turns out that all possible messages
m (0≤m≤n-1) are unconcealed when calculating me mod n.
For any valid choice of e there exist some unconcealed messages.
It's important that the number of unconcealed messages is at a minimum.

Choose p=1009 and q=3643.
Find the sum of all values of e, 1<e<φ(1009,3643) and gcd(e,φ)=1, so that the number of unconcealed messages for this
value of e is at a minimum.
"""

# So the number of unconcealed messages (solutions to x^e = x (mod n) -> x^e - x = 0 (mod n)) is apparently equal to
# (gcd(e-1, p-1) + 1)*(gcd(e-1, q-1) + 1), proven by someone who knows more math than I do
# Also, the possible values of e are the coprimes of phi, generated with a sieve using prime factors of phi
# This solution runs in ~2 seconds

from math import gcd, sqrt

p = 1009
q = 3643

n = p*q
phi = (p - 1)*(q - 1)

def unconcealed(e):
  # I don't have a pure math degree, but Jernej on math.SE says this is correct
  return (gcd(e - 1, p - 1) + 1) * (gcd(e - 1, q - 1) + 1)

def prime_factors(m):
  if m <= 1:
    return []
  
  for fac in range(2, int(sqrt(m)) + 1):
    if m % fac == 0:
      return prime_factors(fac) + prime_factors(m // fac)
  
  return [m]

def gen_coprimes(m): # takes m bytes of memory for the sieve
  factors = set(prime_factors(m))
  sieve = [True for _ in range(m - 1)]
  
  for factor in factors:
    for i in range(factor, m, factor):
      sieve[i-1] = False
  
  yield from (i+1 for i, is_coprime in enumerate(sieve) if is_coprime)

min_unconcealed = 10**10
sum_e = 0

for e in gen_coprimes(phi):
  unc = unconcealed(e)
  
  if unc < min_unconcealed:
    min_unconcealed = unc
    sum_e = e
  elif unc == min_unconcealed:
    sum_e += e

print(sum_e)
