
# Author: Dv8edRoute
# Email: dv8edroute@protonmail.com
# Version 1.1.1
# License: MIT

"""
fiscal445 1.1.1 — 4-4-5 Retail Fiscal Calendar
────────────────────────────────────────────────────────────────────
                         WHAT'S NEW IN 1.1.1
────────────────────────────────────────────────────────────────────
100 % BACKWARDS COMPATIBLE — all 1.0.0 code runs unchanged

New optional capture_outliers flag on Calendar():
   folds the 1-6 "outlier" days that fall outside the normal week grid
   (between Jan 1 / Dec 31 and your nearest fiscal week boundary)
   into week 1 and week 52, so no calendar day goes unaccounted for


────────────────────────────────────────────────────────────────────
                         CARRIED OVER FROM 1.0.0
────────────────────────────────────────────────────────────────────
Full pandas 2.x / 3.x support
100–200× faster calendar generation
Real-world retail behavior: fiscal year starts Jan 1 (any weekday)
   → first week can be partial, first full week ends on your chosen day
Clean, typed, future-proof code while keeping the exact same public API


Thank you for using fiscal445 since 2020
────────────────────────────────────────────────────────────────────
"""

import pandas as pd
import numpy as np
import datetime
import calendar
from datetime import timedelta, datetime
import sys
import re



current = np.datetime_as_string(np.datetime64('today','s'))[:10] # set the current date in numpy datetime
now = datetime.now()

class Calendar(object):
    '''Calendar classes primary function is to dynamically create a dataframe table based on the input date and week ending
    arguments and return a completed dataframe'''

    def __init__(self,begin_year,week_ending,capture_outliers=False):
        # capture_outliers is a NEW parameter, added at the END of the
        # argument list with a default value of False.
        #
        # Why it has to go at the end: Python matches positional arguments
        # left to right. Every existing call in the wild looks like
        # Calendar('2026-01-01','SAT') — only two arguments. Because
        # capture_outliers defaults to False when the caller doesn't
        # supply it, every one of those old two-argument calls keeps
        # working exactly as before, with the new behavior simply off.
        # If we'd inserted it in the middle of the argument list instead,
        # every existing call in every script that uses this package
        # would silently break or misbehave.
        '''Set the variables for the class.

        capture_outliers (default False, fully backward compatible):
        When your fiscal year's start date doesn't fall exactly on your
        week_ending weekday, there are 1-6 "outlier" days between the
        true calendar-year boundary (Jan 1 / Dec 31) and the nearest
        fiscal week boundary. By default those days are simply outside
        the calendar (the old, original behavior). Set this to True to
        fold them into week 1 (at the start) and week 52 (at the end)
        instead, so no calendar day in the year is ever unaccounted for.
        '''
        
        self.begin_year = begin_year
        self.week_ending = week_ending

        # Store the flag on the instance itself (self.capture_outliers),
        # the same pattern already used for begin_year and week_ending
        # above. build() reads this later to decide whether to run the
        # outlier-capture logic at all. Nothing else in the class needs
        # to touch it directly.
        self.capture_outliers = capture_outliers
    #

    def build(self):
        """Takes the arguments from fc5.cal = fc5.Calendar(['first day date of your fiscal year'],
        ['Last fiscal day of the week]) and breaks them down in to smaller variables which create
        a dataframe with three columns. fiscal_month, fiscal_week, week_ending. It populates those
        columns dynamically based on the input it recieves. """

        #Error checking input date and day format

        try:
            start_pattern = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
            day_pattern = re.compile(r"^(MON|TUE|WED|THU|FRI|SAT|SUN)")
            if not start_pattern.match(self.begin_year):
                raise ValueError(' \n First day date of fiscal year malformed in fc5.cal = fc5.Calendar("YYYY-MM-DD","Day").build().\
                     \n Accepted entries are: "YYYY-MM-DD"')
            if not day_pattern.match(self.week_ending.upper()):
                raise ValueError(' \n Last fiscal day of the week malformed in fc5.cal = fc5.Calendar("YYYY-MM-DD","Day").build().\
                     \n Accepted entries are: "Mon,Tue,Wed,Thu,Fri,Sat,Sun"')
        except ValueError as err:
            print(err)
            sys.exit()
        
        lst = self.begin_year.split('-')
        year = lst[0]
        month = lst[1]
        day = lst[2]
        self.week_ending = str(self.week_ending.upper())
        desired_month = int(month)
        year_start = f'{year}-{month}-{day}'
        
        # Creates a list with 52 entries with the 4-4-5 pattern for the fiscal week column
        weeks = []
        four = [1,2,3,4]
        five = [1,2,3,4,5]
        count = 1
        for _ in range(0,13):
            if count in [3,6,9,12]:
                weeks.extend(five)
                count += 1
            else:
                weeks.extend(four)
                count += 1

        # Create the list for the week_ending column using year_start and week_ending vars
        
        cur_year = pd.Series(pd.date_range(year_start, periods=53, freq=f'W-{self.week_ending}'))

        # Creates a list of months based on the input of first fiscal date of the year .

        def _get_month_list(mon_choice, day):
            if int(day) >= 15:
                mon_choice = (mon_choice % 12) + 1
            base = [1,2,3,4,5,6,7,8,9,10,11,12]
            start_idx = mon_choice - 1
            rotated = base[start_idx:] + base[:start_idx]
            rotated.append(rotated[0])

            mon = []
            for i in rotated:
                y = calendar.month_name[i]
                mon.append(y)
            multipliers = [4,4,5,4,4,5,4,4,5,4,4,5,4]
            mon = [x for x, multipliers in zip(mon, multipliers) for _ in range(multipliers)]
            return mon

        mon = _get_month_list(desired_month, day)


        # Complite the three lists in to a list of lists
        newlist = [cur_year,weeks,mon]
        
        # Converts year_start to np.datetime object
        x = np.datetime64(year_start,'s')
        yr_start = np.datetime64(np.datetime_as_string(x)[:10])

        # Creates finished dataframe more efficiently by building a list of rows
        rows = []
        # start row
        rows.append({"week_ending": yr_start,
                     "fiscal_week": 'Start',
                     "fiscal_month": 'Start'})

        # 53 weeks
        for idx in range(0,53):
            line_item = [item[idx] for item in newlist]
            rows.append({
                "week_ending": line_item[0],
                "fiscal_week": line_item[1],
                "fiscal_month": line_item[2]
            })

        self.df = pd.DataFrame(rows, columns=["week_ending", "fiscal_week", "fiscal_month"])

        # Everything below only runs if the caller explicitly opted in.
        # With the default capture_outliers=False, this whole block is
        # skipped entirely, and self.df is returned exactly as it always
        # was — this is what makes the change backward compatible.
        if self.capture_outliers:
            fiscal_year = int(year) + 1 if int(month) == 12 else int(year)
            true_start = pd.Timestamp(fiscal_year, 1, 1)
            true_end   = pd.Timestamp(fiscal_year, 12, 31)

            # --- FRONT of the year ---
            if true_start < self.df.loc[0, 'week_ending']:
                self.df.loc[0, 'week_ending']  = true_start
                self.df.loc[0, 'fiscal_week']  = self.df.loc[1, 'fiscal_week']
                self.df.loc[0, 'fiscal_month'] = self.df.loc[1, 'fiscal_month']

            
            if self.df.loc[52, 'week_ending'] != true_end:
                self.df.loc[52, 'week_ending'] = true_end

        return self.df



@pd.api.extensions.register_dataframe_accessor("show") # allows datframe objects to have additional methods added to them
class Date_functions:
    
    '''This class is aliased by the pandas accessor decorator from "Date_functions" to "show" when calling it from the parent script.
    It contains all of the methods that will act on the cal dataframe and return results to the parent script.
    '''
    
    def __init__(self, pandas_obj):
        '''Set the variables for the class'''
        self._obj = pandas_obj

    def _check_current_in_range(self):
        '''Raises a clear error if `current` (today's real date, or
        whatever date fiscal445 is reading) falls outside the span this
        calendar actually covers. fiscal445 is designed for real-time use
        only -- methods that depend on "today" don't make sense for a
        calendar representing a different year.'''
        start = self._obj.loc[0, 'week_ending']
        end = self._obj.loc[52, 'week_ending']
        now = pd.Timestamp(current)
        if not (start <= now <= end):
            raise RuntimeError(
                f"fiscal445: the current date ({current}) falls outside the "
                f"range of this calendar ({start.strftime('%Y-%m-%d')} to "
                f"{end.strftime('%Y-%m-%d')}). Methods that depend on the "
                f"current date only work for the fiscal year this calendar "
                f"represents."
            )
        
  
    def cur_week_of_month(self):
        '''Usage: fc5.cal.show.cur_week_of_month() 
            Returns an int representing which week of the month based on the 445 calendar and the current date'''
        self._check_current_in_range()
        return self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_week'].head(1).values.item()
    
    def prior_week_of_month(self):
        '''Usage: fc5.cal.show.prior_week_of_month() 
            Returns an int representing which prior week of the month it is based on the 445 calendar and the current date'''
        self._check_current_in_range()
        return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_week'].tail(1).values.item()
    
    def cur_week_of_year(self):
        '''Usage: fc5.cal.show.cur_week_of_year() 
            Returns an int representing which week of the year it is, based on the 445 calendar and the current date'''
        self._check_current_in_range()
        return self._obj.index[self._obj['week_ending'] >= current].tolist()[0]

    
    def cur_month(self,var=None):
        '''Usage: fc5.cal.show.cur_month({optional var}) 
        
        Example: fc5.cal.show.cur_month() 
            Returns a string representing the name of the month ('March') of the year it is, based on the 445 calendar and the current date
            
        With optional var example:  fc5.cal.show.cur_month(3)
             Returns a sliced string, the length based on the optional int value, representing the 
             name of the month ('Mar') of the year it is, based on the 445 calendar and the current date'''
        self._check_current_in_range()
        if var == None:
            return self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_month'].head(1).values.item()
        else:
            return self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_month'].head(1).values.item()[:var]
        
    def month_of_prior_week(self,var=None):
        '''Usage: fc5.cal.show.month_of_prior_week({optional var}) 
        
        Example: fc5.cal.show.month_of_prior_week() 
            Returns a string representing the name of the month ('March') of the year it is, based on the 
            445 calendar and the current date minus one week
            
        With optional var example:  fc5.cal.show.month_of_prior_week(3)
             Returns a sliced string, the length based on the optional int value, representing the 
             name of the month ('Mar') of the year it is, based on the 445 calendar and the current date minus one week'''
        self._check_current_in_range()
        if var == None:
            return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_month'].tail(1).values.item()
        else:
            return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_month'].tail(1).values.item()[:var]
           
    def month_to_date(self):
        '''Usage: fc5.cal.show.month_to_date() 
            Returns a tuple representing the start of the current month and the current date, based on the 445 calendar'''
        self._check_current_in_range()
        idx = self._obj.index[self._obj['week_ending'] >= current].tolist()[0]
        week_pos = self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_week'].tolist()[0]
        new_idx = idx - week_pos
        now_month = self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_month'].head(1).values.item()
        now_month = datetime.strptime(now_month, "%B")
        if now_month.month == 1:
            beginning = self._obj.loc[0, 'week_ending']
            beginning = beginning.strftime("%Y-%m-%d")
        else:
            beginning = self._obj.loc[new_idx, 'week_ending'] + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
        end = current 
        return str(beginning),str(end)

    
    def month_to_date_completed(self):
        '''Usage: fc5.cal.show.month_to_date_completed() 
            Returns a tuple representing the start of the current month and the last date of the last 
            completed week as set by week_ending and based on the 445 calendar and the current date'''
        self._check_current_in_range()
        idx = self._obj.index[self._obj['week_ending'] > current].tolist()[0]
        week_pos = self._obj.loc[self._obj['week_ending'] > current, 'fiscal_week'].tolist()[0]
        new_idx = idx - week_pos
        if new_idx == 0:
            beginning = self._obj.loc[0, 'week_ending']
        else:
            beginning = self._obj.loc[new_idx, 'week_ending'] + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = self._obj.loc[self._obj['week_ending'] < current, 'week_ending'].tolist()[-1]
        end = end.strftime("%Y-%m-%d")
        if end < beginning:
            return 'Not available yet!'
        return str(beginning),str(end)
    
    
    def year_to_date(self):
        '''Usage: fc5.cal.show.year_to_date() 
            Returns a tuple representing the start of the current year and the current date based on the 445 calendar and the current date'''
        self._check_current_in_range()
        beginning = self._obj.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
        return str(beginning),str(end)

    def year_to_date_completed(self):
        '''Usage: fc5.cal.show.year_to_date_completed() 
            Returns a tuple representing the start of the current year and the last date of the last 
            completed week as set by week_ending and based on the 445 calendar and the current date'''
        self._check_current_in_range()
        beginning = self._obj.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = self._obj.loc[self._obj['week_ending'] < current, 'week_ending'].tolist()[-1]
        end = end.strftime("%Y-%m-%d")
        return str(beginning),str(end)


    def quarter_dates(self,val):
        '''Usage: fc5.cal.show.quarter_dates(val)
        val:
        (1) = Q1, (2) = Q2, (3) = Q3, (4) = Q4
        
        Example: fc5.cal.show.quarter_dates(1)   
        
            Returns a tuple representing the start of the choosen quarter and the last day of the choosen quarter based on the 445 calendar'''
        self.val = val
        if self.val == 1:
            beginning = self._obj.loc[0,'week_ending']
            beginning = beginning.strftime("%Y-%m-%d")
            end = self._obj.loc[13,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 2:
            beginning = self._obj.loc[13,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = self._obj.loc[26,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 3:
            beginning = self._obj.loc[26,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = self._obj.loc[39,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 4:
            beginning = self._obj.loc[39,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = self._obj.loc[52,'week_ending']
            end = end.strftime("%Y-%m-%d")
        
        return str(beginning),str(end)

    def quarter_to_date(self,val):
        '''Usage: fc5.cal.show.quarter_to_date(val)
        
        val:
        (1) = Q1, (2) = Q2, (3) = Q3, (4) = Q4
       
        Example: fc5.cal.show.quarter_to_date(1)   
       
            Returns a tuple representing the start of the choosen quarter and the curret date based on the 445 calendar
            should you choose a quarter the is in the future of the current date the function will return
       
            Quarter available yet!'''
        self._check_current_in_range()
        self.val = val
        if self.val == 1:
            beginning = self._obj.loc[0,'week_ending']
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 2:
            beginning = self._obj.loc[13,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 3:
            beginning = self._obj.loc[26,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 4:
            beginning = self._obj.loc[39,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if np.datetime64(end) < np.datetime64(beginning):
            return 'Quarter not available yet!'
        
        return str(beginning),str(end)
