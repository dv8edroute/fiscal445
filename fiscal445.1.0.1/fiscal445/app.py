
# Author: Dv8edRoute
# Email: dv8edroute@protonmail.com
# Version 1.0.1
# License: MIT

"""
fiscal445 1.0.1 — 4-4-5 Retail Fiscal Calendar
────────────────────────────────────────────────────────────────────
                         WHAT'S NEW IN 1.0.1
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
                mon_choice = mon_choice +1
            mlst = [1,2,3,4,5,6,7,8,9,10,11,12,1]
            if mon_choice == 1:
                mon_choice = mlst
            else:
                mon_choice = mon_choice -1
                lst = mlst[mlst.index(mon_choice)+1:]
                lst.extend(mlst[:mon_choice])
                mon_choice = lst


            mon = []
            for i in mon_choice:
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

            # 'year' already exists at this point in build() — it was
            # split out of self.begin_year near the top of the method
            # (the line "year = lst[0]") to build the fiscal-month list.
            # We're reusing that same variable, not creating a new one.
            #
            # pd.Timestamp, not Python's built-in datetime.date: pandas 3
            # is strict about this. The 'week_ending' column is stored as
            # a pandas datetime64 column, and pandas 3 refuses to accept
            # a plain datetime.date value into that column — it raises a
            # TypeError. pd.Timestamp is pandas's own datetime type, so
            # it matches the column's dtype and pandas accepts it.
            true_start = pd.Timestamp(int(year), 1, 1)   # Jan 1 of the fiscal year
            true_end   = pd.Timestamp(int(year), 12, 31) # Dec 31 of the fiscal year

            # --- FRONT of the year ---
            # Row 0 is always the 'Start' placeholder row (see the
            # rows.append({...'fiscal_week': 'Start'...}) block earlier
            # in build()). Its week_ending currently equals begin_year
            # itself — e.g. 2026-01-03 — which is WHY days before that
            # (Jan 1-2) were invisible to the calendar: nothing in the
            # table represented them.
            #
            # We fix that by moving row 0's date back to true Jan 1, and
            # copying week 1's own label onto it. Two effects:
            #  1. Any query for Jan 1 or Jan 2 now finds a row whose date
            #     is >= that query date, and that row correctly reports
            #     week 1 / the first fiscal month, instead of matching
            #     the old 'Start' row and returning the placeholder text
            #     'Start'.
            #  2. year_to_date() and month_to_date() both read row 0's
            #     week_ending directly as their "beginning" date. Since
            #     we changed that cell to Jan 1, those methods now report
            #     the correct start automatically — we don't have to
            #     touch those methods at all.
            self.df.loc[0, 'week_ending']  = true_start
            self.df.loc[0, 'fiscal_week']  = self.df.loc[1, 'fiscal_week']
            self.df.loc[0, 'fiscal_month'] = self.df.loc[1, 'fiscal_month']

            # --- BACK of the year ---
            # Row 52 is week 52, the last "normal" week before the extra
            # leap-week row (row 53) that exists for years needing a 53rd
            # week. Depending on how begin_year lines up with week_ending,
            # week 52 sometimes ends a few days short of Dec 31 (e.g.
            # Dec 29), leaving Dec 30-31 outside any week — the same kind
            # of gap as the front, just at the other end of the year.
            #
            # We only stretch row 52 forward if it's actually short.
            # Some years week 52 already reaches or passes Dec 31 on its
            # own (that happened in our 2026 test) — in that case this
            # condition is False and we correctly leave it untouched.
            if self.df.loc[52, 'week_ending'] < true_end:
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
        
  
    def cur_week_of_month(self):
        '''Usage: fc5.cal.show.cur_week_of_month() 
            Returns an int representing which week of the month based on the 445 calendar and the current date'''
        return self._obj.loc[self._obj['week_ending'] >= current, 'fiscal_week'].head(1).values.item()
    
    def prior_week_of_month(self):
        '''Usage: fc5.cal.show.prior_week_of_month() 
            Returns an int representing which prior week of the month it is based on the 445 calendar and the current date'''
        return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_week'].tail(1).values.item()
    
    def cur_week_of_year(self):
        '''Usage: fc5.cal.show.cur_week_of_year() 
            Returns an int representing which week of the year it is, based on the 445 calendar and the current date'''
        return self._obj.index[self._obj['week_ending'] >= current].tolist()[0]

    
    def cur_month(self,var=None):
        '''Usage: fc5.cal.show.cur_month({optional var}) 
        
        Example: fc5.cal.show.cur_month() 
            Returns a string representing the name of the month ('March') of the year it is, based on the 445 calendar and the current date
            
        With optional var example:  fc5.cal.show.cur_month(3)
             Returns a sliced string, the length based on the optional int value, representing the 
             name of the month ('Mar') of the year it is, based on the 445 calendar and the current date'''
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
        if var == None:
            return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_month'].tail(1).values.item()
        else:
            return self._obj.loc[self._obj['week_ending'] < current, 'fiscal_month'].tail(1).values.item()[:var]
           
    def month_to_date(self):
        '''Usage: fc5.cal.show.month_to_date() 
            Returns a tuple representing the start of the current month and the current date, based on the 445 calendar'''
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
        idx = self._obj.index[self._obj['week_ending'] > current].tolist()[0]
        week_pos = self._obj.loc[self._obj['week_ending'] > current, 'fiscal_week'].tolist()[0]
        new_idx = idx - week_pos
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
        beginning = self._obj.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
        return str(beginning),str(end)

    def year_to_date_completed(self):
        '''Usage: fc5.cal.show.year_to_date_completed() 
            Returns a tuple representing the start of the current year and the last date of the last 
            completed week as set by week_ending and based on the 445 calendar and the current date'''
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
