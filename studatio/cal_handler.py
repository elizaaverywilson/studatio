import calendar
from datetime import datetime

try:
    from . import user_config
    from .user_config import Settings

    from ._vendor.icalevents import icalevents

    from .enums import StudioEventType, Instrument
    from .events import StudioEvent
    from .storage import load_cached_events
except ImportError:
    import user_config
    from user_config import Settings

    from _vendor.icalevents import icalevents

    from enums import StudioEventType, Instrument
    from events import StudioEvent
    from storage import load_cached_events


def export(month: int = datetime.now().month, year: int = datetime.now().year):
    events = fetch_events(year, month)

    parsed_events = parse_events(events)
    combined_events = combine_adjacent_events(parsed_events)

    event_list_string = ''
    for event in combined_events:
        event_list_string = event_list_string + str(event) + '\n'

    return event_list_string


def combine_adjacent_events(events: list):
    events_copy = events
    for event in events_copy:
        try:
            # noinspection PyUnboundLocalVariable
            previous_event
        except NameError:
            previous_event = event
        else:
            if previous_event.end_time == event.start_time and previous_event.kind == event.kind:
                events_copy.remove(previous_event)
                combined_instruments = previous_event.instruments.union(event.instruments)
                combined_event = StudioEvent(start_time=previous_event.start_time,
                                             end_time=event.end_time,
                                             kind=event.kind,
                                             instruments=combined_instruments,
                                             plural=True)

                i = events.index(event)
                events_copy.insert(i, combined_event)
                events_copy.remove(event)

            previous_event = event
    return events_copy


def fetch_events(year: int, month: int):
    cal = calendar.Calendar()
    month_dates_nearby = cal.itermonthdates(year, month)
    month_dates = []

    for date in month_dates_nearby:
        if date.month == month:
            month_dates.append(date)

    settings = Settings()
    calendar_url = settings.calendar_url
    events = icalevents.events(url=calendar_url, fix_apple=True, start=month_dates[0], end=month_dates[-1])
    return events


def _parse_event(ical_event):
    start_time = ical_event.start
    end_time = ical_event.end
    if 'Trial' in ical_event.summary:
        kind = StudioEventType.TRIAL_LESSON
    elif 'Lesson' in ical_event.summary:
        kind = StudioEventType.LESSON
    elif 'Class Performance' in ical_event.summary:
        kind = StudioEventType.CLASS_PERFORMANCE
    elif 'Class' in ical_event.summary:
        kind = StudioEventType.CLASS
    elif 'Dress Recital' in ical_event.summary:
        kind = StudioEventType.DRESS_RECITAL
    elif 'Recital' in ical_event.summary:
        kind = StudioEventType.RECITAL
    else:
        kind = StudioEventType.OTHER

    instruments = set()
    if 'Violin' in ical_event.summary:
        instruments.add(Instrument.VIOLIN)
    if 'Viola' in ical_event.summary:
        instruments.add(Instrument.VIOLA)
    if 'Fiddle' in ical_event.summary:
        instruments.add(Instrument.FIDDLE)

    return StudioEvent(start_time, end_time, kind, instruments)


def parse_events(events):
    parsed_events = []

    for ical_event in events:
        studio_event = _parse_event(ical_event)
        parsed_events.append(studio_event)

    return parsed_events
