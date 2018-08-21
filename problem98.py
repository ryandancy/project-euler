#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 98:

By replacing each of the letters in the word CARE with 1, 2, 9, and 6 respectively, we form a square number: 1296 =
36^2. What is remarkable is that, by using the same digital substitutions, the anagram, RACE, also forms a square
number: 9216 = 96^2. We shall call CARE (and RACE) a square anagram word pair and specify further that leading zeroes
are not permitted, neither may a different letter have the same digital value as another letter.

Using data/p098_words.txt, a 16K text file containing nearly two-thousand common English words, find all the square
anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.
"""

# We map each anagram and each square to a list of indices; i.e. (CARE, RACE) -> ((0, 1, 2, 3), (2, 1, 0, 3)).
# We then use this to match words to squares, then loop to find squares that match both words in the anagramic pair.
# This solution runs in ~0.25 seconds.

def map_to_indices(s, return_dict=False):
  letter_idxs = {}
  idxs = []
  counter = 0
  
  for letter in s:
    if letter not in letter_idxs:
      letter_idxs[letter] = counter
      counter += 1
    idxs.append(letter_idxs[letter])
  
  if return_dict:
    return idxs, letter_idxs
  else:
    return idxs

# Get all the words
with open('data/p098_words.txt', 'r') as word_file:
  content = word_file.readlines()[0][:-1]
  words = list(map(lambda word: word[1:-1], content.split(',')))

# Find all anagram pairs
ordered_words = list(map(tuple, map(sorted, words)))
anagram_pairs = []
seen = {} # word: {idx, ...}
for i, ordered in enumerate(ordered_words):
  if ordered in seen:
    for idx2 in seen[ordered]:
      anagram_pairs.append((words[idx2], words[i]))
    seen[ordered].add(i)
  else:
    seen[ordered] = {i}

# Turn them into lists of indices (i.e. ('CENTRE', 'RECENT') -> ((0, 1, 2, 3, 4, 1), (4, 1, 0, 1, 2, 3)))
anagram_indices = []
for word1, word2 in anagram_pairs:
  word1_idxs, letter_idxs = map_to_indices(word1, return_dict=True)
  word2_idxs = [letter_idxs[letter] for letter in word2]
  anagram_indices.append((tuple(word1_idxs), tuple(word2_idxs)))

# Find all squares less than the max anagram word length
max_length = max([len(word1) for word1, word2 in anagram_pairs])
squares = list(map(str, [n**2 for n in range(int(10**(max_length/2)))]))

# Do the same thing with lists of indices (but map indices -> squares)
square_indices = {}
for square in squares:
  idxs = tuple(map_to_indices(square))
  if idxs in square_indices:
    square_indices[idxs].add(square)
  else:
    square_indices[idxs] = {square}

# Find squares matching anagram pairs
largest_square = 0
for i, (idxs1, idxs2) in enumerate(anagram_indices):
  squares_matching_1 = square_indices[idxs1]
  squares_matching_2 = square_indices[tuple(map_to_indices(idxs2))]
  
  for square in squares_matching_1:
    # Change the square from idxs1 to idxs2
    digit_idxs = {idx: digit for digit, idx in zip(square, idxs1)}
    square_idx2 = ''.join(digit_idxs[i] for i in idxs2)
    
    if square_idx2 in squares_matching_2:
      print('Found:', square, '&', square_idx2, 'for', anagram_pairs[i])
      
      larger = max(int(square), int(square_idx2))
      if larger > largest_square:
        largest_square = larger

print(largest_square)
