'''

Modules main purpose is to dynamically create a 52 week calendar based on the financial ideal of a 4 week month, 4 week month and 5 week month per quarter.
It achieves this by taking input from the parent script and initializing the calendar table.The syntax for this is

import fiscal445 as fc5

fc5.cal = fc5.Calendar(['first day of your fiscal year'],['3 letter last day of your fiscal week']).build() 
 
an example of this is...

fc5.cal = fc5.Calendar('2020-02-02','sat').build()

Once intialized the following meathods can  be run. See individual method docstrings for syntax or readme.md 

NOTE: methods use a pandas api accessor decorator("show") instead of class name Date_functions


fc5.cal.show.cur_week_of_month()
fc5.cal.show.cur_week_of_year()
fc5.cal.show.cur_month()
fc5.cal.show.month_to_date()
fc5.cal.show.month_to_date_completed()
fc5.cal.show.year_to_date()
fc5.cal.show.year_to_date_completed()
fc5.cal.show.quarter_dates(args)
fc5.cal.show.quarter_to_date(args)
 
 '''


from .app import *