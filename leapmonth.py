#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

__doc__ = """\
This function takes the hebrew calendar year as input, and
returns two booleans.

The first returned bool is whether this is a leap year in the
traditional 19 year Metonic cycle, with 7 leap months.

The second returned bool is whether this is a leap year in Irv
Bromberg's rectified hebrew calendar, with a 353-year cycle (with 130
leap months).

For documentation, see

   http://www.sym454.org/hebrew/rect.htm

or

   http://individual.utoronto.ca/kalendis/hebrew/rect.htm
"""

def leapmonth(hyear, do_print=False):
    if hyear < 2500:
        # Assume we've received a CE year
        hyear += 3760

    tradleap = ((7 * hyear + 1) % 19) < 7
    rectleap = ((130 * hyear + 268) % 353) < 130

    if do_print:
        is_is_not = {True:"*IS*", False:"*IS NOT*"}
        print("Hebrew year", hyear,
              is_is_not[tradleap], "a traditional leap year, and",
              is_is_not[rectleap], "a rectified leap year")

    return (tradleap, rectleap)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        year = int(sys.argv[1])
    else:
        year = int(input('Enter hebrew year to be checked ==> '))

    tradleap, rectleap = leapmonth(year, True)
