#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

__doc__ = """\
Usage:   fortnight.py [year month day]

Returns day of week in a fortnight for any Gregorian date, using a
variation of the mental math method from

http://jimvb.home.mindspring.com/doom14.html

which is based on Conway's day of week for any date algorithm from
"Winning Ways for your Mathematical Plays, Volume 2" (1980).
For reference to the original Doomsday Rule, see http://rudy.ca/doomsday.html .

If year, month and day are not provided, input is requested.

The fortnight returned is a number between 0 and 13.

Also returns Left or Right to indicate the 0th or 1st week of the
biweekly cycle.  Base month is chosen to be February 2015, with the
paycheck (Right Friday) on the 2nd and 4th Fridays of the month.

Days 0-6 are Left Sunday through Left Saturday.
Days 7-13 are Right Sunday through Right Saturday.
"""

def fortnight(year, month, day, do_print=False):
    h = year // 100             # integer division for the century
    yy = year % 100             # year within the century

    # Modified century correction
    # Original doomsday c = (5 * (h % 4) + 2) % 7
    # We determine bi-weekly correction by computing the dozens rule
    # for 100 years, with no leap day in non-400 centuries
    c = (12*(h%8) + (h%8)//4 + 2) % 14

    # To reverse L and R, change formula to
    # c = (12*(h%8) + (h%8)//4 + 9) % 14

    # Doomsday reference day for each month, corrected to match
    # the biweekly cycle.
    dd = {1:3, 2:14, 3:14, 4:11, 5:9, 6:6,
          7:4, 8:15, 9:12, 10:10, 11:7, 12:5}[month]

    # January/February correction for leap years
    if month < 3:
        if ((yy % 4) == 0):
            dd += 1

    # Year correction within century using the dozens rule, which
    # gives the correct day of week modulo 14.
    yc = yy // 12 + yy % 12 + (yy%12) // 4

    # Doomsday for the year
    pi_day = (c + yc) % 14

    # Day of week for desired date:
    weekday = (pi_day + (day - dd) + 14) % 14

    def fullname(wd):
        dayname = {0:"Sunday",
                   1:"Monday",
                   2:"Tuesday",
                   3:"Wednesday",
                   4:"Thursday",
                   5:"Friday",
                   6:"Saturday"}
        return {0:"Left", 1:"Right"}[wd//7] + " " + dayname[wd % 7]

    if (do_print):
        print("Year in century (yy) =", yy)
        print("Century correction (c) = (12*({}%8) + ({}%8)/4 + 2)%14 = {}".format(h,h,c))
        print("yc = yy/12 + yy%12 + (yy%12)/4 =",
              yy//12, "+", yy%12, "+", (yy%12)//4, "=", yc)
        print("Pi day for the year = (c + yc) % 14 =",
              pi_day, "({})".format(fullname(pi_day)))
        print("\n\t{:04}/{:02}/{:02} occurs on {}\n".format(year,
                                                            month,
                                                            day,
                                                            fullname(weekday)))
    return weekday

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
    else:
        year = int(input('Enter year ==> '))
        month = int(input('Enter month ==> '))
        day = int(input('Enter day ==> '))

    weekday = fortnight(year, month, day, True)
