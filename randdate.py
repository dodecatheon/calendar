#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

import datetime
from moonphase import moonphase
from doomsday import dayofweek
from random import randint
import sys

__doc__="""\
Test your ability to guess the day of the week and the age of the moon
for a not-quite uniformly random date between 1700 and 2299.
"""

def monthlength(mm, yy, cc):
    if mm in [9,4,6,11]: # 30 days hath September, April, June, and November
        days = 30
    elif mm != 2:               # All the rest have 31
        days = 31
    elif mm == 2:               # Excepting February alone
        days = 28               # Which has 28 days clear
        if ((yy == 0 and cc % 4 == 0) or
            (yy >  0 and yy % 4 == 0)):
            days = 29           # and 29 in each leap year,
            # (as long as it's a year evenly divisible by 400)
    return days

if len(sys.argv) == 4:
    y = int(sys.argv[1])
    m = int(sys.argv[2])
    d = int(sys.argv[3])
    cc = y // 100
    yy = y % 100
else:
    # Create a random date
    cc = randint(17,22)
    yy = randint(0,99)
    m = randint(1,12)
    y = cc * 100 + yy
    d = randint(1, monthlength(m, yy, cc))

randdate = datetime.datetime(year=y, month=m, day=d)

print("{}/{:02}/{:02}\n".format(y,m,d))

actual = randdate.isoweekday() % 7

date_dict = { 0: '0 (Sunday)',
              1: '1 (Monday)',
              2: '2 (Tuesday)',
              3: '3 (Wednesday)',
              4: '4 (Thursday)',
              5: '5 (Friday)',
              6: '6 (Saturday)' }

print("You have three chances to guess the day of the week for that date.")
print("Enter a number between 0 (Sunday) and 6 (Saturday) at the prompt.")
for i in range(3):
    guess = int(input("What day of the week is {}/{:02}/{:02}?  [Attempt # {}] ==> ".format(y,m,d,i+1)))

    print("You guessed", date_dict[guess], ".")

    if guess == actual:
        print("\n\tCongratulations!  You guessed correctly.\n")
        break
    else:
        print("\n\tSorry, that was not correct.  Try again.")

if i == 3:
    print("Actual day of the week for {}/{:02}/{:02} is".format(y,m,d),
          date_dict[actual], "\n")

print("Doomsday Rule calculation:")
doomsday = dayofweek(y, m, d, do_print=True)

if doomsday != actual:
    print("\n\tNote:  Doomsday Rule and datetime.isoweekday() calculate different days!")

mp = moonphase(y, m, d, do_print=False)

print("You have three chances to guess the phase of the moon for that date.")
print("Enter a number between 0 and 29 at the prompt.")
for i in range(3):
    guess = int(input("What is the moon's age on {}/{:02}/{:02}?  [Attempt # {}] ==> ".format(y,m,d,i+1)))

    if guess == mp:
        print("\n\tCongratulations!  You guessed correctly.\n")
        break
    else:
        print("\n\tSorry, that was not correct.  Try again.")

mp = moonphase(y, m, d, do_print=True)
