#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    range = xrange
    input = raw_input
    from itertools import izip as zip
except NameError:
    pass
import ephem

__doc__ = """\
This function takes the CE calendar year as input, and
returns two booleans.

The first returned bool is whether this is a leap year in the
Gregorian calendar.

The second is whether this is a leap year in the continued fraction
approximation calendar, with a year 365 days, 5 hours, 49 minutes long

Zero year is set to 1777 CE, with year one at 1718CE.

This has excellent accuracy for years 1058 through 4297, with only 19
years that miss having spring on 3/21 UT by one day.  The accuracy is
even good enough to get up to 4557 with only one more off year.

In year 4297CE, the calendar should be adjusted for years 4297 tto 5882,
during which the mean equinoctial year changes substantially, to

365 days, 5 hours, 48 minutes, 52.830161717 seconds

which in practice means switching from cycles of 14*33 + 29 to cycles of
5 or 6 * 33 + 29.
"""

def springleap(year, do_print=False):

    # yy = year - 1711
    # while (yy < 0):
    #     yy += 2488
    #
    # z = (((yy % 2488) % 1997) % 491) % 33

    # yy = year - 1319
    # while (yy < 0):
    #     yy += 949
    #
    # z = (((yy % 949) % 458) % 33)

    yy = year - 1777
    while (yy < 0):
        yy += 1440

    z = (((yy % 1440) % 491) % 33)

    if z > 0 and z % 4 == 0:
        rectleap = True
    else:
        rectleap = False

    y = year
    while (y < 0):
        y += 400

    c = y // 100

    tradleap = False
    if y % 100 == 0:
        if y % 400 == 0:
            tradleap = True
    elif y % 4 == 0:
        tradleap = True

    if do_print:
        if year <= 0:
            yyy = year - 1
        else:
            yyy = year

        string = ephem.next_vernal_equinox(str(yyy))
        print(year, tradleap, rectleap, y % 4, z, string)

    return (tradleap, rectleap)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        year = int(sys.argv[1])
    else:
        year = int(input('Enter Gregorian year to be checked ==> '))

    tradleap, rectleap = springleap(year, True)
