# -*- coding: utf-8 -*-
"""
    grigri.dates.range
    ~~~~~~~~~~~~~~~~~~

    Methods for dynamically generating a range of dates e.g. a date range
    for the current month.
"""

from datetime import datetime, timedelta
from functools import partial

import pandas as pd

from .scalar import first_of, end_of

__all__ = [
    'day_range', 'date_range',
    'week_range', 'month_range','quarter_range', 'year_range',
]

def day_range(num_days, anchor_date=None, inclusive=True):
    """
    Returns a range of dates spanning the specified number of 
    days.

    :param num_days: Number of days to move forward (or backwards if negative) 
                     from the `anchor_date`. Corresponds to the length of the 
                     returned date range. 
    :param anchor_date: Datetime to begin counting from.
    :param inclusive: If `True` will include `anchor_date` as part of the
                      date_range

    >>> day_range(-6, datetime(2013,9,5), inclusive=False)
    <class 'pandas.tseries.index.DatetimeIndex'>
    [2013-08-30 00:00:00, ..., 2013-09-04 00:00:00]
    Length: 6, Freq: D, Timezone: None
    """

    assert num_days != 0, 'day_range must span at least one day'

    if anchor_date is None:
        anchor_date = datetime.now()

    shift = 1 if num_days > 0 else -1

    swing_date = anchor_date + timedelta(num_days - shift)

    if not inclusive:
        anchor_date += timedelta(shift)
        swing_date += timedelta(shift)

    if anchor_date > swing_date:
        anchor_date, swing_date = swing_date, anchor_date 

    return pd.date_range(anchor_date, swing_date, normalize=True)

def date_range(dt=None, freq='m', full_range=True):
    """
    Returns a date range for the specified frequency e.g. all the 
    dates in a particular month or quarter.

    :param dt: Datetime that determines the time period to use
    :param freq: Frequency of the time period e.g. 'w', 'm' or 'q'
    :param full_range: If `True` will return a date range for the 
                        entire period. Otherwise, it will return a 
                        date range from the first of the period up 
                        to `dt`.
    """

    if dt is None:
        dt = datetime.now()

    start_date = first_of(dt=dt, freq=freq)
    end_date = end_of(dt=dt, freq=freq) if full_range else dt

    return pd.date_range(start_date, end_date, normalize=True)

week_range = partial(date_range, freq='w')
month_range = partial(date_range, freq='m')
quarter_range = partial(date_range, freq='q')
year_range = partial(date_range, freq='y')