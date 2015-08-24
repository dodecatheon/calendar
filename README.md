# calendar
python scripts to implement Conway "mental math" calculators for dates

I recently discovered a number of algorithms by John H. Conway that can be
used for mental calculation.  Most of these were described in

Winning Ways for Your Mathematical Plays, Vol. 2
by Elwyn R. Berlekamp (Author), John H. Conway (Author), Richard K. Guy (Author)

published in 1983 and revised in 2003.

This repo is to collect python scripts I wrote to implement the algorithms,
which helps me remember how to do them mentally and also check whether I'm
getting them correct.

Install the ```ephem``` package for optional astronomical calculation checks.

```doomsday.py```:  enter year, month and date at the commandline to see the
Doomsday rule calculation.

```moonphase.py```: enter year, month and date at the commandline to see
Conway's moon phase approximation calculation.

```paschal.py```: enter year at the commandline to see how to calculate
estimated date of Easter Sunday that year.

```randdate.py```: generates a random date between 1700 and 2299 to test your
command of the Gregorian calendar Doomsday Rule and the moon phase
calculation.

```fortnight.py```: Adaptation of the Doomsday Rule to calculate fortnights
(14 day payday periods).

```leapmonth.py```:  Enter either a Jewish calendar year or a Gregorian year
to see if a leap month of Adar will be inserted in the spring, and whether
that it is "correct" or "incorrect" according to the Bromberg Jewish calendar
correction.  For example, ```leapmonth.py 2016``` has the output ```5776 True
False```, which means that there will be a leap lunar month inserted in early
2016, but it will incorrectly cause the full moon of Nisan to occur more than
one lunar month after the first day of spring.

```contfrac.py```: Calculates the continued fraction approximation for a given
decimal number.  Try, for example:  ```contfrac.py 3.14159265358979323845```.
The result demonstrates that 355/113 is a very good approximation to pi.
