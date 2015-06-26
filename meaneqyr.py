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

def gregtuple(year):

    if year < 1:
        yy = year - 1
    else:
        yy = year
    return ephem.next_vernal_equinox(str(yy)).tuple()

def seconds(h, m, s):
    return h*3660. + m*60. + s

if __name__ == "__main__":
    import sys
    import contfrac

    baseyear = int(sys.argv[1])

    years = 0
    leaps = 0
    for tt in sys.argv[2:]:
        t = int(tt)
        years += t*33 + 29
        leaps += t*8 + 7

    finalyear = baseyear + years
    days = years * 365 + leaps

    basetup = gregtuple(baseyear)
    endtup = gregtuple(finalyear)

    adjust = ( seconds(*endtup[3:6]) -
               seconds(*basetup[3:6]) ) / 86400.

    print("\tBase year =", baseyear, ", final year =", finalyear)
    print("\tMean eq. year ~= ", days, "/", years)
    print("\twith", leaps, "leap years.\n")
    print("\t{}".format(days), "days modulo 7 =", days % 7)

    approx = (days + adjust) / float(years)
    print("\tAdjusted days =", days + adjust)
    print("\tbasetup =", basetup)
    print("\tendtup =", endtup)
    print("\tDecimal mean eq. year =", approx)

    frac = (days + adjust) / float(years)

    dd = int(frac)
    hh = int((frac - dd) * 24.)
    mm = int((frac - dd - hh/24.) * 1440.)
    ss = ((frac - dd - hh/24. - mm/1440.) * 86400.)

    print("Mean eq. year = {} days, {} hours, {} minutes, {} seconds".format(dd,hh,mm,ss))

    contfrac.main(frac)
