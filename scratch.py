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

print(sys.argv)
if len(sys.argv) == 2:
    r1 = 1
    r2 = int(*sys.argv[1])
elif len(sys.argv) == 3:
    r1 = int(sys.argv[1])
    r2 = int(sys.argv[2])
else:
    r1 = 1
    r2 = 7000

if r1 < 1:
    yc = -1
else:
    yc = 0

springs = []
for y in range(r1,r2):
    tup = gregtuple(y)
    tupp4 = gregtuple(y+4)
    if tup[3] == 0 and tupp4[3] > 20:
        springs.append(tup)
#
last29 = r1 - 144
tupm1 = (r1-12,1,1,1,1,1)
count = 0
lastdiff33 = 4
leaps = 0
for tup in springs:
    diff = tup[0] - tupm1[0]
    tupm1 = tup

    if tup[0] < 179:
        z = ((tup[0] + 143) % 161) % 33
    if tup[0] < 1058:
        z = ((tup[0] - 179) % 260) % 33
    elif tup[0] < 4297:
        # 2 cycles of 14*33+29 plus 1 cycle of 13*33+29
        z = ((((tup[0]-1776 + 1440)) % 1440) % 491) % 33 # 19
    elif tup[0] < 5304:
        # 3 cycles of 7*33 + 29 plus 1 cycle of 6*33 + 29:
        z = (((tup[0]-4297) % 1007) % 260) % 33
    elif tup[0] < 5465:
        # 4*33 + 29
        z = ((tup[0] - 5304) % 161) % 33
    elif tup[0] < 6456:
        # 7 cycles of 3*33 + 29
        z = ((tup[0] - 5465) % 128) % 33
    elif tup[0] < 6803:
        # 2*33 + 29
        z = ((tup[0] - 6456) % 95) % 33
    else:
        # 33 + 29
        z = ((tup[0] - 6803) % 62) % 33
    if diff == 33:
        lastdiff33 += 1
    else:
        lastdiff = tup[0] - last29
        last29 = tup[0]
        leaps += lastdiff33 * 8 + diff // 4
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

print('Count = ', count)
