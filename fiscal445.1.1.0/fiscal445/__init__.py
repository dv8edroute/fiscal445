"""
The fiscal445 package builds a 52-week 4-4-5 fiscal calendar table and
provides convenience methods for common reporting periods.

Basic usage:

    import fiscal445 as fc5

    # Initialize the fiscal calendar table
    fc5.cal = fc5.Calendar('2020-02-02', 'sat').build()

    # Once initialized, the following methods can be run via the
    # pandas accessor "show" (registered on the calendar DataFrame).

    fc5.cal.show.cur_week_of_month()
    fc5.cal.show.prior_week_of_month()
    fc5.cal.show.cur_week_of_year()
    fc5.cal.show.cur_month()
    fc5.cal.show.month_of_prior_week()
    fc5.cal.show.month_to_date()
    fc5.cal.show.month_to_date_completed()
    fc5.cal.show.year_to_date()
    fc5.cal.show.year_to_date_completed()
    fc5.cal.show.quarter_dates(args)
    fc5.cal.show.quarter_to_date(args)
"""

from .app import Calendar, Date_functions  # noqa: F401

__all__ = ["Calendar", "Date_functions"]
__version__ = "1.1.0"
