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
from datetime import datetime

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
def diffmod(year, offset, *mods):
    z = year - offset
    while z < 0:
        z += mods[0]
    for mod in mods:
        z %= mod
    return z, (z > 0 and z % 4 == 0)

def springleap(year, do_print=False):

    # The type of modulo we use depends on the interval this
    # year falls in.
    for yearbin in [1059, 4298, 5305, 5466, 6457, 6804, 50000]:
        if year < yearbin:
            break

    # print("yearbin =", yearbin)

    # extract the appropriate offset and moduli to use for the appropriate
    # year bin.
    mods = {1059:(18,260,33),            # repeat cycles of 3*33 + 29
            4298:(1777,1440,491,33),     # 2 cycles of 14*33+29 plus 1 cycle of 13*33+29
            5305:(4298,1007,260,33),     # 3 cycles of 7*33 + 29 plus 1 cycle of 6*33 + 29:
            5466:(5305,161,33),          # 4*33 + 29
            6457:(5466,128,33),          # 7 cycles of 3*33 + 29
            6804:(6457,95,33),           # 2*33 + 29
            50000:(6804,62,33)}[yearbin] # 33 + 29

    # print("mods =", mods)

    z, rectleap = diffmod(year, *mods)

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

        print(year,
              tradleap,
              rectleap,
              y % 4,
              z,
              ephem.next_vernal_equinox(str(yyy)))

    return (tradleap, rectleap)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        year = int(sys.argv[1])
    else:
        print("Using this year")
        today = datetime.now()
        year = today.year

    tradleap, rectleap = springleap(year, True)
