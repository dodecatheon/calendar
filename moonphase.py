#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass
from datetime import datetime

__doc__ = """\
Usage:   moonphase.py [year month day]

Using calculator from

http://gmmentalgym.blogspot.com/2013/01/moon-phase-for-any-date.html

which is based on Conway's moon phase algorithm from "Winning Ways for
your Mathematical Plays, Volume 2" (1980).

Estimate the age of the moon from 0 to 29 for a particular date
29,30=0,1 new moon
2-6 waxing crescent
7-8 first quarter
9-13 waxing gibbous
14-16 full
17-21 waning gibbous
22-23 last quarter
24-28 waning (de)crescent

If year, month and day are not provided, input is requested.

Handles years from 1700 to 3099.
"""
hmonths = {
    12: 'ADAR',
    5 : 'AV',
    6 : 'ELUL',
    8 : 'HESHVAN',
    2 : 'IYYAR',
    9 : 'KISLEV',
    1 : 'NISAN',
    11: 'SHEVAT',
    3 : 'SIVAN',
    4 : 'TAMMUZ',
    10: 'TEVETH',
    7 : 'TISHRI',
    13: 'VEADAR' }

def moonphase(year, month, day, do_print=False):
    h = year // 100             # integer division for the century
    yy = year % 100             # year within the century

    # The "golden number" for this year is the year modulo 19, but
    # adjusted to be centered around 0 -- i.e., -9 to 9 instead
    # of 0 to 19.  This improves the accuracy of the approximation
    # to within +/- 1 day.
    g = (yy + 9) % 19 - 9

    # There is an interesting 6 century near-repetition in the
    # century correction.  It would be interesting to find a
    # algorithm that handles the different corrections between
    # centuries 17|23|29, 20|26, 21|27, and 24|30.

    try:
        c = {17:7,
             18:1, 19:-4, 20:-8, 21:16, 22:11, 23:6,
             24:1, 25:-4, 26:-9, 27:15, 28:11, 29:6,
             30:0}[h]
    except KeyError:
        print("No century correction available for {}00-{}99".format(h,h))
        return

    # Golden number correction:  modulo 30, from -29 to 29.
    gc = g * 11
    while ( gc < -29 ): gc += 30;
    if (gc > 0): gc %= 30;

    # January/February correction:
    if month < 3:
       mc = 2
    else:
       mc = 0

    phase = (month + mc + day + gc + c + 30 ) % 30

    if (do_print):
        # It's nice to see what the Golden correction for the year
        # plus the century correction is.  This lets us quickly calculate the
        # correction for any other date in the same year.
        gcpc = (gc + c) % 30
        if gcpc <= 0:
            gcpc_alt = gcpc + 30
        else:
            gcpc_alt = gcpc - 30

        print("yy =", yy)
        print("g =", g)
        print("month + day + mc =", month + day + mc)
        print("gc =", gc)
        print("c =", c)
        print("Dates in the year", year,
              "have moon phase correction gc + c =",
              gcpc, "or", gcpc_alt)
        print(("\n\t{:04}/{:02}/{:02} has "
               "estimated moon phase = {}\n").format(year,
                                                   month,
                                                   day,
                                                   phase))
        if phase < 2:
            print("\tNew moon [or slightly after]")
        elif phase < 7:
            print("\tWaxing crescent")
        elif phase < 9:
            print("\tFirst quarter")
        elif phase < 14:
            print("\tWaxing gibbous")
        elif phase < 16:
            print("\tFull moon")
        elif phase < 22:
            print("\tWaning gibbous")
        elif phase < 24:
            print("\tLast quarter")
        elif phase < 29:
            print("\tWaning (de)crescent")
        elif phase < 31:
            print("\tNew moon [or slightly before]")

        try:
            # If you have the ephem package installed, you
            # can compare the estimate to the actual lunar phase
            import ephem
            thisdate = ephem.Date('{:04}/{:02}/{:02} 00:00:01'.format(year, month, day))
            prevmoon = ephem.previous_new_moon(thisdate)
            nextmoon = ephem.next_new_moon(thisdate)
            prevfull = ephem.previous_full_moon(thisdate)
            nextfull = ephem.next_full_moon(thisdate)
            prevymd = prevmoon.tuple()[:3]
            nextymd = nextmoon.tuple()[:3]
            pfymd = prevfull.tuple()[:3]
            nfymd = nextfull.tuple()[:3]
            print("\n\t{}".format(prevmoon), "UTC = Previous New Moon")
            print("\t{}".format(nextmoon), "UTC = Next New Moon")
            print("\t{}".format(prevfull), "UTC = Previous Full Moon")
            print("\t{}".format(nextfull), "UTC = Next Full Moon")
            try:
                from convertdate import julianday
                thisjdc = julianday.from_gregorian(year, month, day)
                prevjdc = julianday.from_gregorian(*prevymd)
                nextjdc = julianday.from_gregorian(*nextymd)
                pfjdc = julianday.from_gregorian(*pfymd)
                nfjdc = julianday.from_gregorian(*nfymd)
                print("\t{:2} days since prev new moon".format(int(thisjdc - prevjdc)))
                print("\t{:2} days until next new moon".format(int(nextjdc - thisjdc)))
                print("\t{:2} days since prev full moon".format(int(thisjdc - pfjdc)))
                print("\t{:2} days until next full moon".format(int(nfjdc - thisjdc)))
            except:
                print("julianday doesn't work")
                pass
        except:
            pass

        try:
            # If you have convertdate installed, you can compare the lunar
            # phase to the hebrew calendar date:
            from convertdate import hebrew
            hyear, hmonth, hday = hebrew.from_gregorian(year, month, day)
            print("\n\tHebrew date = {} {}, {}\n".format( hday,
                                                          hmonths[hmonth],
                                                          hyear ))
        except:
            pass
    return phase

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
    else:
        print("Using today's date")
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day

    phase = moonphase(year, month, day, True)
