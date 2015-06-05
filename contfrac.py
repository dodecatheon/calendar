#!/usr/bin/env python
# Python 3 compatibility
from __future__ import print_function, division
try:
    range = xrange
    input = raw_input
except NameError:
    pass

__doc__ = """\
Print out continued fraction terms of a decimal fraction, with
rational approximations.
"""
from math import log10, floor, sqrt

# Default constants
MAX_PLACES = 8
EPS = 1.e-14

# TO DO:  Figure out how to turn this into a generator
def continued_fraction(x, max_places=MAX_PLACES, eps=EPS):
    x_orig = x
    small = sqrt(eps)

    # Initialize:
    a = int(x)
    (pm1, p) = (1, a)
    (qm1, q) = (0, 1)

    terms = [(a,p,q)]

    for i in range(1,100):

        # Subtract off integer part from previous iteration
        x -= a

        # Don't divide by small number
        if (abs(x) < small):
            break

        # Start next continued fraction iteration
        x = 1. / x

        # Capture fractions that are very close to 1
        a = int(x + small)

        # Calculate next approximate numerator and denominator pair:
        (pm1, p) = (p, a * p + pm1)
        (qm1, q) = (q, a * q + qm1)

        # Halt loop if numerator or denominator is too big:
        if ((floor(log10(p)) > max_places) or
            (floor(log10(q)) > max_places)):
            break

        # Save results
        terms.append((a,p,q))

        # Calculate approxmation and deviation from original
        approx = float(p) / q
        err = approx - x_orig

        if abs(err) < eps or a == 0:
            break

    return terms

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        x = float(sys.argv[1])
    else:
        x = float(input('Enter x to be approximated ==> '))

    fmt = ( " a_{i:02} = {a:5} ; "
            "x ~= {p:10} / {q:10} "
            "= {approx:20.15f}, "
            "err = {err:+13.8e}" )

    print("Continued fraction terms, with rational approximations:")

    for i, (a, p, q) in enumerate(continued_fraction(x)):

        # Calculate approxmation and deviation from original
        approx = float(p) / q
        err = approx - x

        print(fmt.format(i=i,
                         a=a,
                         p=p,
                         q=q,
                         approx=approx,
                         err=err))
