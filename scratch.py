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
    # z = (((tup[0]-1058 + 2158) % 2158) % 425) % 33
    # z = ((((tup[0]-1710 + 2488*3) % 2488) % 1997) % 491) % 33  # count = 18
    z = (((((tup[0]-1318 + 949*5)) % 949) % 458) % 33) # count = 17
    print('{:4}, {:2}, {:2}, {}'.format(tup[0], diff, z, tup[1:]))
    if 1058 <= tup[0] <= 3872:
        if z != 0:
            count += 1
    tupm1 = tup

print('Count = ', count)
