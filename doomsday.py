#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

__doc__ = """\
Usage:   doomsday.py [year month day]

Returns day of week for any Gregorian date, using mental math method from

http://rudy.ca/doomsday-links.html

which is based on Conway's day of week for any date algorithm from
"Winning Ways for your Mathematical Plays, Volume 2" (1980).

If year, month and day are not provided, input is requested.
"""

def dayofweek(year, month, day, do_print=False):
    h = year // 100             # integer division for the century
    yy = year % 100             # year within the century

    c = (5 * (h % 4) + 2) % 7   # Century correction

    # Doomsday reference day for each month
    dd = {1:3, 2:14, 3:14, 4:4, 5:9, 6:6,
          7:11, 8:8, 9:5, 10:10, 11:7, 12:12}[month]

    # January/February correction for leap years
    if month < 3:
        if ((yy % 4) == 0):
            dd += 1

    # Year correction within century using the dozens rule
    yc = yy // 12 + yy % 12 + (yy%12)//4

    # Doomsday for the year
    pi_day = (c + yc) % 7

    # Day of week for desired date:
    weekday = (pi_day + (day - dd) + 28) % 7

    if (do_print):
        dayname = {0:"Sunday",
                   1:"Monday",
                   2:"Tuesday",
                   3:"Wednesday",
                   4:"Thursday",
                   5:"Friday",
                   6:"Saturday"}
        #
        print("\nYear in century (yy) =", yy)
        print("Century correction (c) =", c)
        print("\nYear in century correction (yc), using the dozens rule:")
        print("\tyc = yy/12 + yy%12 + (yy%12)/4 =",
              yy//12, "+", yy%12, "+", (yy%12)//4, "=", yc)
        # Alternative calculation for yc
        print(("\nCalculating the year-in-century correction with "
               "the 'odd plus 11' rule:"))
        oddp11 = (yy + (yy%2)*11) // 2
        print("\t({} + {}*11) / 2 = {}".format(yy, yy%2,oddp11))
        o1 = oddp11
        oddp11 = (o1 + (o1%2)*11) % 7
        print("\t({} + {}*11) % 7 = {}".format(o1, o1%2, oddp11))
        o2 = oddp11
        oddp11 = 7 - oddp11
        print("\t7 - {} = {}".format(o2, oddp11))
        print("\nPi day for the year = (c + yc) % 7 =",
              pi_day, "({})".format(dayname[pi_day]))

        print("\nPi day reference for the month is {:02}/{:02}".format(month,dd))

        print("Specified day is {} days from the monthly pi-day".format(day - dd))

        print("\n\t{:04}/{:02}/{:02} falls on a {}\n".format(year,
                                                            month,
                                                            day,
                                                            dayname[weekday]))
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

    weekday = dayofweek(year, month, day, True)
