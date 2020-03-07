# Author: Dv8edRoute
# Email: dv8edroute@protonmail.com
# Version 0.0.1
# License: MIT

import pandas as pd
import numpy as np
import datetime
import calendar
from datetime import timedelta  


x = np.datetime64('today','s')
#x= np.datetime64('2021-03-12','s')
current = np.datetime64(np.datetime_as_string(x)[:10])


def set_445_cal(begin_year,week_ending):
    lst = begin_year.split('-')
    year = lst[0]
    month = lst[1]
    day = lst[2]
    week_ending = str(week_ending.upper())
    desired_month = int(month)
    year_start = f'{year}-{month}-{day}'
    
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

    
    cur_year = pd.Series(pd.date_range(year_start, periods=52, freq=f'W-{week_ending}'))
    

    # Get list of Months

    def get_month_list(mon_choice, day):
        if int(day) >= 10:
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



    newlist = [cur_year,weeks,mon]
    
    x = np.datetime64(year_start,'s')
    yr_start = np.datetime64(np.datetime_as_string(x)[:10])

    df = pd.DataFrame()
    df = df.append({"week_ending" : yr_start , "fiscal_week" : 'Start',"fiscal_month": 'Start' } , ignore_index=True)
    for x in range(0,52):
        line_item = [item[x] for item in newlist]
        temp =pd.DataFrame([line_item],columns=["week_ending", "fiscal_week", "fiscal_month"])
        df = df.append(temp, ignore_index=True)

    return df



def week_of_month():
    return cal.loc[cal['week_ending'] >= current, 'fiscal_week'].head(1).item()

def cur_fiscal_week_of_year():
    return cal.index[cal['week_ending'] >= current].tolist()[0]


def cur_fiscal_month():
    return cal.loc[cal['week_ending'] >= current, 'fiscal_month'].head(1).item()


def month_to_date():
    idx = cal.index[cal['week_ending'] >= current].tolist()[0]
    week_pos = cal.loc[cal['week_ending'] >= current, 'fiscal_week'].tolist()[0]
    new_idx = idx - week_pos
    beginning = cal.loc[new_idx, 'week_ending'] + timedelta(days=1)
    beginning = beginning.strftime("%Y-%m-%d")
    end = current 
    return str(beginning),str(end)


def month_to_date_completed():
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



def year_to_date():
    beginning = cal.loc[0,'week_ending']
    beginning = beginning.strftime("%Y-%m-%d")
    end = current 
    return str(beginning),str(end)


def year_to_date_completed():
    beginning = cal.loc[0,'week_ending']
    beginning = beginning.strftime("%Y-%m-%d")
    end = cal.loc[cal['week_ending'] < current, 'week_ending'].tolist()[-1]
    end = end.strftime("%Y-%m-%d")
    return str(beginning),str(end)


def quarter_completed(q):
    if q == 1:
        beginning = cal.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[13,'week_ending']
        end = end.strftime("%Y-%m-%d")
    if q == 2:
        beginning = cal.loc[13,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[26,'week_ending']
        end = end.strftime("%Y-%m-%d")
    if q == 3:
        beginning = cal.loc[26,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[39,'week_ending']
        end = end.strftime("%Y-%m-%d")
    if q == 4:
        beginning = cal.loc[39,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = cal.loc[52,'week_ending']
        end = end.strftime("%Y-%m-%d")
    
    return str(beginning),str(end)

def quarter_to_date(q):
    if q == 1:
        beginning = cal.loc[0,'week_ending']
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
    if q == 2:
        beginning = cal.loc[13,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
    if q == 3:
        beginning = cal.loc[26,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
    if q == 4:
        beginning = cal.loc[39,'week_ending']  + timedelta(days=1)
        beginning = beginning.strftime("%Y-%m-%d")
        end = current 
    if np.datetime64(end) < np.datetime64(beginning):
        return 'Quarter available yet!'
    
    return str(beginning),str(end)



# cal = set_445_cal('2020-02-02','sat')
# cal.to_excel('test/test_df.xlsx', header=True, index=False)