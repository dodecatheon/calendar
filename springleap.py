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
approximation calendar, with the mean equinoctial year averaged from 1710
to 4297, as follows:

$ meaneqyr.py 1710 12 15 16 19 12

	Base year = 1710 , final year = 4297
	Mean eq. year ~=  944882 / 2587
	with 627 leap years.

	944882 days modulo 7 = 1
	Adjusted days = 944881.994132
	basetup = (1710, 3, 21, 0, 34, 40.812683841213584)
	endtup = (4297, 3, 20, 0, 26, 13.82541038095951)
	Decimal mean eq. year = 365.242363406
Mean eq. year = 365 days, 5 hours, 49 minutes, 0.198304108889 seconds
Continued fraction terms, with rational approximations:
 a_00 =   365 ; x ~=        365 /          1 =  365.000000000000000, err = -2.42363406e-01
 a_01 =     4 ; x ~=       1461 /          4 =  365.250000000000000, err = +7.63659370e-03
 a_02 =     7 ; x ~=      10592 /         29 =  365.241379310344826, err = -9.84095953e-04
 a_03 =     1 ; x ~=      12053 /         33 =  365.242424242424249, err = +6.08361267e-05
 a_04 =    14 ; x ~=     179334 /        491 =  365.242362525458248, err = -8.80839309e-07
 a_05 =     4 ; x ~=     729389 /       1997 =  365.242363545317971, err = +1.39020415e-07
 a_06 =     1 ; x ~=     908723 /       2488 =  365.242363344051455, err = -6.22461016e-08
 a_07 =     1 ; x ~=    1638112 /       4485 =  365.242363433667776, err = +2.73702199e-08
 a_08 =     1 ; x ~=    2546835 /       6973 =  365.242363401692216, err = -4.60534011e-09
 a_09 =     3 ; x ~=    9278617 /      25404 =  365.242363407337450, err = +1.03989350e-09
 a_10 =     1 ; x ~=   11825452 /      32377 =  365.242363406121626, err = -1.75930381e-10
 a_11 =     4 ; x ~=   56580425 /     154912 =  365.242363406321033, err = +2.34763320e-11
 a_12 =     1 ; x ~=   68405877 /     187289 =  365.242363406286529, err = -1.10276233e-11
 a_13 =     1 ; x ~=  124986302 /     342201 =  365.242363406302161, err = +4.60431693e-12
 a_14 =     1 ; x ~=  193392179 /     529490 =  365.242363406296647, err = -9.09494702e-13
 a_15 =     3 ; x ~=  705162839 /    1930671 =  365.242363406297613, err = +5.68434189e-14

Zero year is set to 1711 CE, with year one at 1712CE.
We stop the approximation at a_06, for an approximate year =
365.242363344051455 = 365 days 05:49:0.1929260457103732

This has pretty good accuracy for years 1711 through 4200, with only a
few 4 or 5 year periods that miss having spring on 3/21 UT by one day.

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

    yy = year - 1319
    while (yy < 0):
        yy += 949

    z = (((yy % 949) % 458) % 33)

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
