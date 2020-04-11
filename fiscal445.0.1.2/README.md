
# fiscal445

## Description

This script was developed to simplify the determination of reporting dates when using a 445 financial calendar. Many companies use the 445 calendar for financial reporting and it is difficult when setting up reports for YTD, MTD, by quarter runs while only relying on a standard calendar. This module simplifies this by allowing you to set your own  start of the year date and weekending day.

## Prerequisites
Built and tested using

python 3.6+, 
pandas 0.25.3+, 
numpy 1.18.0, 
datetime,
sys,

## Deployment
General Deployment


python -m pip install fiscal445



## Usage

### Import the module

```python
import fiscal445 as fc5
```

#### Set the modules parameters.

To initialize the 445 calendar table

Syntax: `fc5.cal = fc5.Calendar('YYYY-MM-DD','day').build()` where the date is the start of your fiscal 445 year and the day arg is the the last day of your fiscal week.

#### Examples:

```python
fc5.cal = fc5.Calendar('2020-02-02','sat').build()
```


Week of the month it is based on 445 fiscal calendar

```python
fc5.cal.show.cur_week_of_month()
```
returns `1` based on example date

<br>

Week of the year it is based on 445

```python
fc5.cal.show.cur_week_of_year()
```
returns `5` 

<br>
Which month of the year it is based on 445 calendar


```python
fc5.cal.show.cur_month({optional arg})
```
returns `'March'` without optional arg

With optional arg example:  `fc5.cal.show.cur_month(3)`
Returns a sliced string, where the length is based on the optional int arg, representing the name of the month ('Mar') of the year it is, based on the 445 calendar'''

<br>

Start and end for month to date


```python
fc5.cal.show.month_to_date()
```
Returns a tuple of the start and end date for month to date reports

`('2020-03-01', '2020-03-09')`

<br>


Start and end for month to date most recent week completed


```python
fc5.cal.show.month_to_date_completed()
```

returns a tuple of the start and end date for month to date reports for up to the most completed week

`('2020-03-01', '2020-03-08')`

returns the following if there has not been an entire complete fiscal week for that month. 

`'Not available yet!'`

<br>

Start and end for year to date


```python
fc5.cal.show.year_to_date()
```

returns a tuple 

`('2020-02-02', '2020-03-07')`

<br>

Start and end for year to date most recent week completed


```python
fc5.cal.show.year_to_date_completed
```

returns a tuple 

`('2020-02-02', '2020-02-29')`

<br>

Start and end dates for completed quarters.

1 for Q1, 2 for Q2, 3 for Q3, 4 for Q4

arg is int value for quarter indicated above. `fc5.cal.show.quarter_dates(arg)`


```python
fc5.cal.show.quarter_dates(1)
```

returns a tuple 

`('2020-02-02', '2020-05-02')`

<br>

Start and end for quarter to date.

1 for Q1, 2 for Q2, 3 for Q3, 4 for Q4

arg is int value for quarter above. `fc5.cal.show.quarter_to_date(arg)`


```python
fc5.cal.show.quarter_to_date(1)
```

returns a tuple 

`('2020-02-02', '2020-03-07')`

returns the following if the current date is before the requested quarter 

`'Quarter not available!'`

<br>

To view the entire calendar after you have initialized it.

`print(fc5.cal)`


## Authors
Dv8edRoute - Original code

## License
MIT

## Acknowledgments


