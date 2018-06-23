#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Euler Problem 19:

You are given the following information, but you may prefer to do some research for yourself.

* 1 Jan 1900 was a Monday.
* Thirty days has September,
  April, June and November.
  All the rest have thirty-one,
  Saving February alone,
  Which has twenty-eight, rain or shine.
  And on leap years, twenty-nine.
* A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""

def is_leap_year(year):
  return year % 400 == 0 if year % 100 == 0 else year % 4 == 0

# -10**10 because it's February (a special case) and if it gets used, something has gone horribly wrong
MONTH_DAYS = [31, -10**10, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def days_in_month(month, year):
  if month == 1:
    # February
    return 29 if is_leap_year(year) else 28
  else:
    return MONTH_DAYS[month]

# The week starts at Monday (0) and ends at Sunday (6)
SUNDAY = 6

start_weekday = 0
month = 0
year = 1900

starting_sundays = 0

while year < 2001:
  while month < 12:
    start_weekday = (start_weekday + days_in_month(month, year)) % 7
    if start_weekday == SUNDAY and 1901 <= year <= 2000:
      starting_sundays += 1
    month += 1
  year += 1
  month = 0

print(starting_sundays)
