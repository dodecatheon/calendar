#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

from jdcal import gcal2jd
from math import pi, sin
from datetime import datetime

__doc__ = """\
Usage:   ecliptlong.py [yyyy mm dd]

Returns ecliptic longitude for specified date.

If year, month and day are not provided, current date is assumed.
"""

def ecliptlong(year, month, day, do_print=False):
   # See https://en.wikipedia.org/wiki/Position_of_the_Sun#Ecliptic_coordinates
   # Days since Jan 1, 2000:
    n = sum(list(gcal2jd(year,month,day)) + [0.5]) - 2451545.0
    L = 280.460 + 0.9856474 * n
    while L > 360.:
        L -= 360.
    while L < 0.:
        L += 360.

    L_rad = (L / 180.) * pi
    g = 357.528 + 0.9856003 * n
    while g > 360.:
        g -= 360.
    while g < 0.:
        g += 360.
    g_rad = (g / 180.) * pi

    lam = L + 1.915 * sin(g_rad) + 0.020 * sin(2*g_rad)

    if (do_print):
        seasons = { 0:'SPRING',
                    1:'SUMMER',
                    2:'AUTUMN',
                    3:'WINTER' }

        astrosign = lam / 30.
        octant = lam / 45.
        season = seasons[int(octant//2) % 4]
        xquarter = seasons[((octant+1)%8)//2]
        print("For day = {:04}/{:02}/{:02}:".format(year, month,day))
        print("ecliptic longitude =", lam)
        print("astrological sign position =", astrosign)
        print("ecliptic octant =", octant)
        print("astronomical season =", season)
        print("cross-quarter season =", xquarter)
        try:
            from convertdate import persian
            pyear, pmonth, pday = persian.from_gregorian(year, month, day)
            print("Persian date = {} {}, {}".format(pday,
                                                    {1:'aries',
                                                     2:'taurus',
                                                     3:'gemini',
                                                     4:'cancer',
                                                     5:'leo',
                                                     6:'virgo',
                                                     7:'libra',
                                                     8:'scorpio',
                                                     9:'sagittarius',
                                                     10:'capricorn',
                                                     11:'aquarius',
                                                     12:'pisces'}[pmonth],
                                                    pyear))
        except:
            pass
    return lam

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
    else:
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day

    lam = ecliptlong(year, month, day, True)
