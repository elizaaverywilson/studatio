import calendar
from datetime import date, timedelta

try:
    from . import user_config
    from .user_config import Settings

    from ._vendor.icalevents import icalevents

    from .events import StudioEvent, MonthYear
    from .storage import load_cached_events
except ImportError:
    import user_config
    from user_config import Settings

    from _vendor.icalevents import icalevents

    from events import StudioEvent, MonthYear
    from storage import load_cached_events


def export_schedule(month_years: [MonthYear], settings: Settings) -> str:
    events_str = ''

    i = 1
    for month_year in month_years:
        if i > 1:
            events_str += '\n'
        events_str += _export_month_schedule(month_year, settings)
        i += 1

    return events_str


def _export_month_schedule(month_year: MonthYear, settings: Settings) -> str:
    events = _fetch_combined(month_year, settings)

    events_str = ''
    for event in events:
        events_str += event.__str__([]) + '\n'

    return events_str


def format_hours_minutes(delta: timedelta) -> [int]:
    if delta < timedelta(0):
        raise ValueError
    return [delta.days * 24 + delta.seconds // 3600, (delta.seconds // 60) % 60]


def elapsed_in_months(month_years: [MonthYear], settings: Settings) -> timedelta:
    delta_sum = timedelta(0)

    for month_year in month_years:
        events = _fetch_parsed(month_year, settings)
        delta_sum += _add_elapsed_from_events(events)

    return delta_sum


def _add_elapsed_from_events(events: [StudioEvent]) -> timedelta:
    delta_sum = timedelta(0)

    for event in events:
        delta_sum += event.end_time - event.start_time

    return delta_sum


def _fetch_parsed(month_year: MonthYear, settings: Settings) -> [StudioEvent]:
    fetched_events = _fetch_events(month_year, settings)
    return _parse_events(fetched_events, settings)


def _fetch_events(month_year: MonthYear, settings: Settings) -> [icalevents.Event]:
    month_dates = _days_of_month(month_year)
    calendar_url = settings.calendar_url
    events = icalevents.events(url=calendar_url, fix_apple=True, start=month_dates[0], end=month_dates[-1])
    return events


def _days_of_month(month_year: MonthYear) -> [date]:
    cal = calendar.Calendar()
    month_dates_nearby = cal.itermonthdates(month_year.year, month_year.month)
    month_dates = []

    for month_date in month_dates_nearby:
        if month_date.month == month_year.month:
            month_dates.append(month_date)

    return month_dates


def _parse_event(ical_event: icalevents.Event, settings: Settings) -> StudioEvent:
    start_time = ical_event.start
    end_time = ical_event.end

    event_type = None
    for e_type in settings.event_types:
        if e_type in ical_event.summary:
            event_type = e_type
            break

    instruments = set()
    for instrument in settings.instruments:
        if instrument in ical_event.summary:
            instruments.add(instrument)

    return StudioEvent(start_time, end_time, event_type, instruments)


def _parse_events(events: [icalevents.Event], settings: Settings) -> [StudioEvent]:
    parsed_events = []

    for ical_event in events:
        studio_event = _parse_event(ical_event, settings)
        parsed_events.append(studio_event)

    return parsed_events


def _combine_adjacent_events(events: [StudioEvent]) -> [StudioEvent]:
    events_copy = events
    for event in events_copy:
        try:
            # noinspection PyUnboundLocalVariable
            previous_event
        except NameError:
            previous_event = event
        else:
            if previous_event.end_time == event.start_time and previous_event.event_type == event.event_type:
                events_copy.remove(previous_event)
                combined_instruments = previous_event.instruments.union(event.instruments)
                combined_event = StudioEvent(start_time=previous_event.start_time,
                                             end_time=event.end_time,
                                             event_type=event.event_type,
                                             instruments=combined_instruments,
                                             plural=True)

                i = events.index(event)
                events_copy.insert(i, combined_event)
                events_copy.remove(event)

            previous_event = event
    return events_copy


def _fetch_combined(month_year: MonthYear, settings: Settings) -> [StudioEvent]:
    parsed = _fetch_parsed(month_year, settings)
    return _combine_adjacent_events(parsed)
