#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

__doc__ = """\
Date of the ecclesiastical paschal moon in any Gregorian year
Use Conway's Doomsday Rule to find the date of the following Sunday.
"""
from math import log10, floor, sqrt

def paschal(year, do_print=False):
    h = year // 100
    g = year % 19 + 1

    c = h//4 + (8*(h+11))//25 - h

    offset = (11 * g + c) % 30

    offset_correction = 0
    if ( offset == 0 ) :
        offset_correction +=1
    if ( offset == 1 ) :
        if g > 12:
            offset_correction += 1

    day = 50 - offset - offset_correction

    if (day > 31):
        month = 4
        day -= 31
    else:
        month = 3

    if do_print:
        monthname = {3:"March", 4:"April"}[month]
        print("\tFor year = CCYY =", year)
        print("\tGolden number = year % 19 + 1 =", g)
        print("\tCentury correction =", c)
        print("\tOffset from 50 = (g*11 + c) % 30 =", offset)
        print("\tOffset correction =", offset_correction)
        print("\tPaschal moon falls on", monthname, day)
        try:
            # Print the moonphase if it is available
            from moonphase import moonphase
            phase = moonphase(year, month, day)
            print("\tMoon phase on that day =", phase)
        except:
            pass

    return (month, day)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        year = int(sys.argv[1])
    else:
        year = int(input('Enter year to be approximated ==> '))

    month, day = paschal(year, True)

    try:
        from doomsday import dayofweek
        dayname = {0:"Sunday",
                   1:"Monday",
                   2:"Tuesday",
                   3:"Wednesday",
                   4:"Thursday",
                   5:"Friday",
                   6:"Saturday"}
        weekday = dayofweek(year, month, day)
        print("\tPaschal moon falls on a", dayname[weekday])

        # find the next Sunday
        day += (7 - weekday + 6) % 7 + 1
        if day > 31:
            day -= 31
            month += 1

        monthname = {3:"March", 4:"April"}
        print("\tEaster {} falls on".format(year),
              monthname[month], day)
    except:
        pass
