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
import sys
from doomsday import dayofweek as dow

__doc__ = """\
Script to determine best year to insert leap week.
"""

def gregtuple(year):

    # if year < 1:
    #     yy = year - 1
    # else:
    #     yy = year
    yy = year
    tup = list(ephem.next_vernal_equinox(str(yy)).tuple())
    # tup[0] = year
    return tuple(tup)

def springdow(year):
    return dow(*gregtuple(year)[:3])

def hour_of_week(year):
    g = gregtuple(year)
    d = dow(*g[:3])
    # Week starts at 10:00 UTC Sunday, at noon Jerusalem time.  This puts
    # the average equinox at Thursday 00:00 Jerusalem (22:00 UTC Wednesday).
    h = (d * 24 + g[3] + (168 - 10)) % 168
    return h, g

z0 = 0
print(sys.argv)
if len(sys.argv) == 2:
    r1 = 1
    r2 = int(*sys.argv[1])
elif len(sys.argv) == 3:
    r1 = int(sys.argv[1])
    r2 = int(sys.argv[2])
elif len(sys.argv) == 4:
    r1 = int(sys.argv[1])
    r2 = int(sys.argv[2])
    z0 = int(sys.argv[3])
else:
    r1 = 1627
    r2 = 2500

if r1 < 1:
    yc = -1
else:
    yc = 0

springs = []
for y in range(r1,r2):
    h, g = hour_of_week(y)
    hp1, gp1 = hour_of_week(y+1)
    if hp1 < h:
        springs.append(gp1)

lastleap = r1 - 5
tupm1 = (lastleap,1,1,1,1,1)
count = 0
totalleaps = 0

#
# Leap year rule ensures northern equinox either falls in UTC
# "spring week", or a leap week is added to ensures it falls in the
# next week.  Use d=118 to match actual equinox times up to 4727.
#
def isleap(y,d):
    if y < 4900:
        return (93*y + d) % 524 < 93
    else:
        return (52*y + d) % 293 < 52

do_calc = False
if do_calc:
    mincount = 525
    d_min = -1
    for d in range(524):
        count = 0
        for tup in springs:
            if not isleap(tup[0],d):
                count += 1
        if count < mincount:
            mincount = count
            d_min = d

    print("d_min = ", d_min, ", mincount = ", mincount)
else:
    # d_min = 67
    d_min = 44

diff_m1 = 6
diff_m2 = 5
sev = 0
threes = 0
for tup in springs:
    diff = tup[0] - tupm1[0]
    tupm1 = tup
    totalleaps += 1
    if tup[0] < 4900:
        d_min = 67
    else:
        d_min = 44
    z = isleap(tup[0],d_min)
    t1 = 0
    t2 = 0
    if diff == 5 and diff_m1 == 6 and diff_m2 == 5:
        t2 = sev
        if sev == 3:
            threes += 1
        elif sev != 0:
            t1 = threes
            threes = 0
        sev = 0
    elif diff == 6 and diff_m1 == 6 and diff_m2 == 5:
        sev += 1

    diff_m1, diff_m2 = diff, diff_m1

    print(('({:4} - '
           '{:4}) = '
           '{:4}, '
           '{:2}, '
           '{}, '
           '{}, '
           '{}, '
           '{}').format(tup[0] + 1,
                        tup[0] - diff + 1,
                        diff,
                        dow(*tup[:3]),
                        z,
                        t1, t2,
                        tup))

print('totalleaps = ', totalleaps)
