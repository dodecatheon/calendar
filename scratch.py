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

springs = []
for y in range(1,7001):
    tup = gregtuple(y)
    tupp4 = gregtuple(y+4)
    if tup[3] == 0 and tupp4[3] != 0:
        springs.append(tup)
#
tupm1 = (-11,1,1,1,1,1)
count = 0
for tup in springs:
    diff = tup[0] - tupm1[0]
    tupm1 = tup
    if tup[0] < 1058:
        z = ((tup[0] - 18) % 260) % 33
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
    print('{:4}, {:2}, {:2}, {}'.format(tup[0], diff, z, tup[1:]))
    if z != 0:
        count += 1

print('Count = ', count)
