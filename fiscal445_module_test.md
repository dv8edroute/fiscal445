#### Import the module

```python
import fiscal445 as fc5
```

##### Set the modules parameters.

###### This will initialize the table using the date provided.
###### Syntax: `fc5.cal = fc5.set_445_cal('YYYY-MM-DD','day')` where the date is the start of your fiscal 445 year and the day arg is the the last day of your fiscal week.

##### Examples:

```python
fc5.cal = fc5.set_445_cal('2020-02-02','sat')
```


###### Week of the month it is based on 445 fiscal calendar

```python
fc5.week_of_month()
```
###### returns `1` based on example date

<br>


###### Week of the year it is based on 445

```python
fc5.cur_fiscal_week_of_year()
```
###### returns `5` 

<br>

###### Which month of the year it is based on 445 calendar


```python
fc5.cur_fiscal_month()
```
###### returns `'March'`


###### Start and end for month to date


```python
fc5.month_to_date()
```
###### Returns as a list the start and end date for month to date reports

###### `('2020-03-01', '2020-03-09')`
<br>


###### Start and end for month to date most recent week completed or (closed)


```python
fc5.month_to_date_completed()
```

###### Returns as a list the start and end date for month to date reports for up to the most completed week

###### `('2020-03-01', '2020-03-08')`

###### Returns the following if there has not been an entire complete fiscal week for that month. 

###### `'Not available yet!'`

<br>

###### Start and end for year to date


```python
fc5.year_to_date()
```

##### Returns as a list 

###### `('2020-02-02', '2020-03-07')`



##### Start and end for year to date most recent week completed (closed)


```python
fc5.year_to_date_completed()
```

##### Returns as a list 

###### `('2020-02-02', '2020-02-29')`


