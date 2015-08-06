#!/usr/bin/env python
# Python 2/3 compatibility:
from __future__ import print_function, division
try:
    input = raw_input
except NameError:
    pass

import radar
import datetime
from moonphase import moonphase

start = datetime.datetime(year=1753, month=1, day=1)
stop = datetime.datetime(year=2300,month=1,day=1)
randdate = radar.random_datetime(start=start, stop=stop)

y, m, d = [int(x) for x in randdate.isoformat()[:10].split('-')]

print(y, m, d)

foo = input('Mentally calculate the day of the week, then hit enter to check it:')

print({ 0: '(0) Sunday',
        1: '(1) Monday',
        2: '(2) Tuesday',
        3: '(3) Wednesday',
        4: '(4) Thursday',
        5: '(5) Friday',
        6: '(6) Saturday' }[randdate.isoweekday() % 7])

foo = input('Mentally calculate the phase of the moon, then hit enter to check it:')

mp = moonphase(y, m, d, do_print=True)
