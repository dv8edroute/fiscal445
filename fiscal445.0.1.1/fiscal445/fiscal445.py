# Author: Dv8edRoute
# Email: dv8edroute@protonmail.com
# Version 0.1.1
# License: MIT

'''

Modules main purpose is to dynamically create a 52 week calendar based on the financial ideal of a 4 week month, 4 week month and 5 week month per quarter.
It achieves this by taking input from the parent script and initializing the calendar table.The syntax for this is

import fiscal445 as fc5

fc5.cal = fc5.Calendar(['first day of your fiscal year'],['3 letter last day of your fiscal week']).build() 
 
an example of this is...

fc5.cal = fc5.Calendar('2020-02-02','sat').build()

Once intialized the following meathods can  be run. See individual method docstrings for syntax or readme.md 

NOTE: methods use a pandas api accessor ("show") 


cal.show.cur_week_of_month()
cal.show.cur_week_of_year()
cal.show.cur_month()
cal.show.month_to_date()
cal.show.month_to_date_completed()
cal.show.year_to_date()
cal.show.year_to_date_completed()
cal.show.quarter_completed(args)
cal.show.quarter_to_date(args)
 
 '''


import pandas as pd
import numpy as np
import datetime
import calendar
from datetime import timedelta
import sys


current = np.datetime_as_string(np.datetime64('today','s'))[:10] # set the current date in numpy datetime
cal = pd.DataFrame() # set empty dataframe

class Calendar(object):
    '''Calendar classes primary function is to dynamically create a dataframe table based on the inputted date and week ending
    arguments and return a completed dataframe'''
    
    def __init__(self,begin_year,week_ending):
        '''Set the variables for the class'''
        
        self.begin_year = begin_year
        self.week_ending = week_ending
    
    def build(self):
        '''Takes the arguments from fc5.cal = fc5.Calendar(['first day of your fiscal year'] and breaks them down in to smaller variables which create a dataframe 
        with three columns. fiscal_month, fiscal_week, week_ending. It populates those columns dynamically based on the input it recieves. '''
        lst = self.begin_year.split('-')
        year = lst[0]
        month = lst[1]
        day = lst[2]
        self.week_ending = str(self.week_ending.upper())
        desired_month = int(month)
        year_start = f'{year}-{month}-{day}'
        
        # This section creates a list with 52 entries with the 4-4-5 pattern for the fiscal week column
        weeks = []
        four = [1,2,3,4]
        five = [1,2,3,4,5]
        count = 1
        for _ in range(0,12):
            if count in [3,6,9,12]:
                weeks.extend(five)
                count += 1
            else:
                weeks.extend(four)
                count += 1

        # Create the list for the week_ending column using year_start and week_ending vars
        cur_year = pd.Series(pd.date_range(year_start, periods=52, freq=f'W-{self.week_ending}'))
        

        # Creates a list of months based on the input of first fiscal date of the year .

        def get_month_list(mon_choice, day):
            if int(day) >= 15:
                mon_choice = mon_choice +1
            mlst = [1,2,3,4,5,6,7,8,9,10,11,12]
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
            multipliers = [4,4,5,4,4,5,4,4,5,4,4,5]
            mon = [x for x, multipliers in zip(mon, multipliers) for _ in range(multipliers)]
            return mon

        mon = get_month_list(desired_month, day)


        # Complite the three lists in to a list of lists
        newlist = [cur_year,weeks,mon]
        
        # Converts year_start to np.datetime object
        x = np.datetime64(year_start,'s')
        yr_start = np.datetime64(np.datetime_as_string(x)[:10])

        #Creates finished dataframe by appending the start ddte to index 0 and adding new rows form from list of lists and returns a dataframe
        self.df = pd.DataFrame()
        self.df = self.df.append({"week_ending" : yr_start , "fiscal_week" : 'Start',"fiscal_month": 'Start' } , ignore_index=True)
        for x in range(0,52):
            line_item = [item[x] for item in newlist]
            temp =pd.DataFrame([line_item],columns=["week_ending", "fiscal_week", "fiscal_month"])
            self.df = self.df.append(temp, ignore_index=True)

        return self.df



@pd.api.extensions.register_dataframe_accessor("show") # allows datframe objects to have additional methods added to them
class Date_functions:
    
    '''This class is aliased by the pandas accessor from "Date_functions" to "show" when calling it from the parent script.
    It contains all of the methods that will act on the cal dataframe and return results to the parent script.
    '''
    
    def __init__(self, pandas_obj):
        '''Set the variables for the class'''
        self._obj = pandas_obj
        cal = self._obj
        
    def cur_week_of_month(self):
        '''Usage: fc5.cal.show.cur_week_of_month() 
            Returns an int representing which week of the month based on the 445 calendar it is currently'''
        return cal.loc[cal['week_ending'] >= current, 'fiscal_week'].head(1).item()       

    def cur_week_of_year(self):
        '''Usage: fc5.cal.show.cur_week_of_year() 
            Returns an int representing which week of the year it is, based on the 445 calendar'''
        return cal.index[cal['week_ending'] >= current].tolist()[0]


    def cur_month(self,var=None):
        '''Usage: fc5.cal.show.cur_month({optional var}) 
        
        Example: fc5.cal.show.cur_month() 
            Returns a string representing the name of the month ('March') of the year it is, based on the 445 calendar
            
        With optional var example:  fc5.cal.show.cur_month(3)
             Returns a sliced string, the length based on the optional int value, representing the 
             name of the month ('Mar') of the year it is, based on the 445 calendar'''
        if var == None:
            return cal.loc[cal['week_ending'] >= current, 'fiscal_month'].head(1).item()
        else:
            return cal.loc[cal['week_ending'] >= current, 'fiscal_month'].head(1).item()[:var]
            
    def month_to_date(self):
        '''Usage: fc5.cal.show.month_to_date() 
            Returns a tuple representing the start of the current month and the current date it is, based on the 445 calendar'''
        idx = cal.index[cal['week_ending'] >= current].tolist()[0]
        week_pos = cal.loc[cal['week_ending'] >= current, 'fiscal_week'].tolist()[0]
        new_idx = idx - week_pos
        beginning = cal.loc[new_idx, 'week_ending'] + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
        return str(beginning),str(end)


    def month_to_date_completed(self):
        '''Usage: fc5.cal.show.month_to_date_completed() 
            Returns a tuple representing the start of the current month and the last date of the last 
            completed week as set by week_ending and based on the 445 calendar'''
        idx = cal.index[cal['week_ending'] > current].tolist()[0]
        week_pos = cal.loc[cal['week_ending'] > current, 'fiscal_week'].tolist()[0]
        new_idx = idx - week_pos
        beginning = cal.loc[new_idx, 'week_ending'] + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[cal['week_ending'] < current, 'week_ending'].tolist()[-1]
        end = end.strftime("%Y-%m-%d")
        if end < beginning:
            return 'Not available yet!'
        return str(beginning),str(end)



    def year_to_date(self):
        '''Usage: fc5.cal.show.year_to_date() 
            Returns a tuple representing the start of the current year and the current date based on the 445 calendar'''
        beginning = cal.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
        return str(beginning),str(end)


    def year_to_date_completed(self):
        '''Usage: fc5.cal.show.year_to_date_completed() 
            Returns a tuple representing the start of the current year and the last date of the last 
            completed week as set by week_ending and based on the 445 calendar'''
        beginning = cal.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[cal['week_ending'] < current, 'week_ending'].tolist()[-1]
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
            beginning = cal.loc[0,'week_ending']
            beginning = beginning.strftime("%Y-%m-%d")
            end = cal.loc[13,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 2:
            beginning = cal.loc[13,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = cal.loc[26,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 3:
            beginning = cal.loc[26,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = cal.loc[39,'week_ending']
            end = end.strftime("%Y-%m-%d")
        if self.val == 4:
            beginning = cal.loc[39,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = cal.loc[52,'week_ending']
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
            beginning = cal.loc[0,'week_ending']
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 2:
            beginning = cal.loc[13,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 3:
            beginning = cal.loc[26,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if self.val == 4:
            beginning = cal.loc[39,'week_ending']  + timedelta(days=1)
            beginning = beginning.strftime("%Y-%m-%d")
            end = current 
        if np.datetime64(end) < np.datetime64(beginning):
            return 'Quarter not available yet!'
        
        return str(beginning),str(end)



if __name__ == '__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--help':
        print(__doc__)

    help(Calendar)
    help(Date_functions )
