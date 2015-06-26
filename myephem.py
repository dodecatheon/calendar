#!/usr/bin/env python
import ephem
from itertools import izip as zip
from pprint import pprint
range = xrange

mytups = []

for yr in range(1,4001):
    tup = ephem.next_vernal_equinox(str(yr)).tuple()
    if tup[3] == 0:
        tup2 = ephem.next_vernal_equinox(str(yr+4)).tuple()
        if tup2[3] != 0:
            mytups.append(tup)

yrs = [tup[0] for tup in mytups]

diffs = [(b,(b-a),tup[1:]) for a, b, tup in zip(yrs[:-1], yrs[1:], mytups[1:])]

pprint(diffs)
