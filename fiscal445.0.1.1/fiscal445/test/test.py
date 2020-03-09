import fiscal445 as fc5

fc5.cal = fc5.Calendar('2020-02-02','sat').build()
print(fc5.cal.show.cur_week_of_month())
print(fc5.cal.show.cur_week_of_year())
print(fc5.cal.show.cur_month(3))
print(fc5.cal.show.month_to_date())
print(fc5.cal.show.month_to_date_completed())
print(fc5.cal.show.year_to_date())
print(fc5.cal.show.year_to_date_completed())
print(fc5.cal.show.quarter_dates(1))
print(fc5.cal.show.quarter_to_date(1))
