# Author: Dv8edRoute
# Email: dv8edroute@protonmail.com
# Version 1.0.1
# License: MIT

import pandas as pd
import numpy as np
import datetime


# Create 445 year fiscal dataset

data = {'January':['1', '2', '3', '4','x'], 'February':['5', '6','7','8','x'], 'March':['9','10','11','12','13'],

        'April':['14', '15', '16', '17','x'], 'May':['18', '19','20','21','x'], 'June':['22','23','24','25','26'],

        'July':['27', '28', '29', '30','x'], 'August':['31', '32','33','34','x'], 'September':['35','36','37','38','39'],

        'October':['40', '41', '42', '43','x'], 'November':['44', '45','46','47','x'], 'December':['48','49','50','51','52'], }

# Create DataFrame

fiscal445df = pd.DataFrame(data, index =['Wk1', 'Wk2', 'Wk3', 'Wk4', 'Wk5'])


def select_rows(fiscal445df,search_strings):
    '''Part of the module. No user value'''
    unq,IDs = np.unique(fiscal445df,return_inverse=True)
    unqIDs = np.searchsorted(unq,search_strings)
    return fiscal445df[((IDs.reshape(fiscal445df.shape) == unqIDs[:,None,None]).any(-1)).all(0)]

def month_lookup(date, length=None) -> int:
    '''Used to determine which month it is based on the 445 fiscal year
    taking a int value of week of year.
    
    Usage: month_lookup(int value of a week of the year, optional length in int of desired month string length)
    Returns a string of month name based on the 445 fiscal calendar'''
    if date == int(date):
        date = str(date)
    for cols in fiscal445df.columns: #enumerate each column in to cols 
        for value in fiscal445df[cols]: #enumerate each column value to value
            if value==date: #check if column value equals input value 
                return cols[:length] # return the column name
            
def week_lookup(date) -> int:
    '''Used to determine which 445 fiscal week it is from a standard calendar week
    
    Usage: week_lookup(int value of a week of the year)
    Returns a string value of the 445 fiscal week of that month ie. Wk1'''
    if date == int(date):
        date = str(date)
    rows = select_rows(fiscal445df,[date]).index.tolist() 
    rows = ''.join(rows)
    return rows

def week_current():
    '''A variable that returns the current week of the year in int format'''
    return datetime.datetime.now().isocalendar()[1]

