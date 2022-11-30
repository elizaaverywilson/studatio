import datetime

import hypothesis as hyp
from hypothesis import strategies as st

from studatio.events import StudioEvent, MonthYear


@st.composite
def st_example_urls(draw):
    return draw(st.text(min_size=1))


@st.composite
def st_month_years(draw):
    month = draw(st.integers(min_value=1, max_value=12))
    # year max_value must be below MAXYEAR, because calendar.itermonth may return dates one year higher.
    year = draw(st.integers(min_value=datetime.MINYEAR, max_value=datetime.MAXYEAR - 1))
    return MonthYear(month, year)


@st.composite
def st_hours(draw):
    return draw(st.integers(min_value=0, max_value=1000000))


@st.composite
def st_minutes(draw):
    return draw(st.integers(min_value=0, max_value=59))


@st.composite
def st_month_opts(draw):
    """
    Strategy for generating a month argument.

    Returns either None, or a tuple with the first argument being the name of the option called,
    and the second being the month, or a string in the form of an integer month, a hyphen, and another integer.
    """
    if draw(st.booleans()):
        if draw(st.booleans()):
            opt_str = '-m'
        else:
            opt_str = '--month'
        if draw(st.booleans()):
            value = draw(st.integers(1, 12))
        else:
            first_month = draw(st.integers(1, 11))
            second_month = draw(st.integers(2, 12))
            if first_month >= second_month:
                hyp.reject()
            value = str(first_month) + '-' + str(second_month)
        return tuple([opt_str, value])
    else:
        return None


@st.composite
def st_year_opts(draw):
    """
    Strategy for generating a year argument.

    Returns either None, or a tuple with the first argument being the name of the option called,
    and the second being the year.
    """
    if draw(st.booleans()):
        if draw(st.booleans()):
            opt_str = '-y'
        else:
            opt_str = '--year'
        return tuple([opt_str, draw(st.integers(1, 9999))])
    else:
        return None


@st.composite
def st_studio_events(draw):
    event_times = draw(st.lists(st.datetimes()))
    events = []

    for event_time in event_times:
        try:
            events.append(StudioEvent(start_time=event_time))
        except NotImplementedError:
            hyp.reject()

    return events


@st.composite
def st_studio_events(draw):
    event_time = draw(st.datetimes())
    try:
        event = (StudioEvent(start_time=event_time))
    except NotImplementedError:
        hyp.reject()

    return event
