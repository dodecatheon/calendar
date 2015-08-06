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

def gregtuple(year):

    # if year < 1:
    #     yy = year - 1
    # else:
    #     yy = year
    yy = year
    tup = list(ephem.next_vernal_equinox(str(yy)).tuple())
    # tup[0] = year
    return tuple(tup)

def minofday(year):
    g = gregtuple(year)
    m = g[3]*60 + g[4]
    return m, g

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
    r1 = 1
    r2 = 7000

if r1 < 1:
    yc = -1
else:
    yc = 0

springs = []
for y in range(r1,r2):
    m, g = minofday(y)
    mp4, gp4 = minofday(y+4)
    ## Midnight to Midnight UTC rule:
    #if tup[3] == 0 and tupp4[3] > 20:
    #    springs.append(tup)
    ## 4PM to 4PM UTC rule, which puts equinox
    ## between sunset to sunset Jerusalem time
    ## So spring will always start between 16:00 UTC 3/20 and 16:00 UTC 3/21
    ## if tup[3] == 16 and tupp4[3] < 16:
    ##    springs.append(tup)
    # Persian calendar rule using 3.5 hours ahead of UTC and day starting
    # at noon Persian time (8:30 UTC = 510 minutes into UT day)
    if m >= 510 and mp4 < 510:
        springs.append(g)
#
# last29 = r1 - 144
last29 = r1 - 5
# tupm1 = (r1-12,1,1,1,1,1)
tupm1 = (last29,1,1,1,1,1)
count = 0
# lastdiff33 = 4
lastdiff33 = 0
leaps = 0
totalleaps = 0
for tup in springs:
    diff = tup[0] - tupm1[0]
    tupm1 = tup

    # if tup[0] < 179:
    #     z = ((tup[0] + 143) % 161) % 33
    # if tup[0] < 1058:
    #     z = ((tup[0] - 179) % 260) % 33
    # elif tup[0] < 4297:
    #     # 2 cycles of 14*33+29 plus 1 cycle of 13*33+29
    #     z = ((((tup[0]-1776 + 1440)) % 1440) % 491) % 33 # 19
    # elif tup[0] < 5304:
    #     # 3 cycles of 7*33 + 29 plus 1 cycle of 6*33 + 29:
    #     z = (((tup[0]-4297) % 1007) % 260) % 33
    # elif tup[0] < 5465:
    #     # 4*33 + 29
    #     z = ((tup[0] - 5304) % 161) % 33
    # elif tup[0] < 6456:
    #     # 7 cycles of 3*33 + 29
    #     z = ((tup[0] - 5465) % 128) % 33
    # elif tup[0] < 6803:
    #     # 2*33 + 29
    #     z = ((tup[0] - 6456) % 95) % 33
    # else:
    #     # 33 + 29
    #     z = ((tup[0] - 6803) % 62) % 33

    # Simplified 8*33 + 29 = 293 year cycle with 71 leap days, centered
    # around year zero = 2235:
    # z = ((tup[0] - 2234 + 2930) % 293 ) % 33
    # z = ((tup[0] - z0 + 2931) % 293 ) % 33

    # Alternate simplified 15*33 + 29 = 524 year cycle with 127 leap
    # days.  Best alignment when z0 = 1656.
    # Also zero modulo 7:  93 leap weeks
    # Good agreement from year 1004 to 4540.
    z = ((tup[0] - z0 + 5241) % 524 ) % 33
    if diff == 33:
        lastdiff33 += 1
    else:
        lastdiff = tup[0] - last29
        last29 = tup[0]
        leaps = lastdiff33 * 8 + diff // 4
        totalleaps += leaps
        print(('{:4}, '
               '{:2}, '
               '{:2}, '
               '({:4} - '
               '{:4}) = '
               '{:4} = '
               '{:2} * 33 + {:2}, '
               '{:4}, '
               '{}').format(tup[0]+1,
                            diff,
                            z,
                            tup[0] + 1,
                            tup[0] - lastdiff + 1,
                            lastdiff,
                            lastdiff33,
                            diff,
                            leaps,
                            tup))
        lastdiff33 = 0
    if z != 0:
        count += 1

print('Count = ', count, ', totalleaps = ', totalleaps)
