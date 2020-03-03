
# fiscal445

## Description

This script was developed to simplify the determination of where in the 445 financial calendar the current week was. Many companies use the 445 calendar for financial reporting and it is difficult when setting up reports for month to date runs while only relying on a standard calendar.

## Prerequisites
Built and tested using

python 3.6+, 
pandas 1.13.0, 
numpy 1.18.0, 
datetime, 

## Deployment
Not uploaded to pypi yet, local use only

## Usage
import fiscal445 as fc5

fc5.weekCurrent()

This will return the current iso week of the year in int format

fc5.monthLookup(date, *length=None*)

First arg is mandatory and it is an int value of the iso week of the calendar year and returns the current month based
on the 445 financial calendar
Second arg is optional, it is also an int defines the length of the returned month name, i.e. 3 = Jan, 5 = Janur and so on

fc5.weekLookup(date)

First arg is mandatory and it is an int value of the iso week of the calendar year, it will return the week
of the month based on the 445 financial calendar, i.e. fc5.weekLookup(9) return Wk1


## Authors
Dv8edRoute - Original code

## License
MIT

## Acknowledgments

Thanks to **Divakar** for the select_rows code snippet from Stack overflow
