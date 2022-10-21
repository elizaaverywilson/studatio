import calendar
from datetime import datetime

try:
    from . import user_config
    from .user_config import Settings

    from ._vendor.icalevents import icalevents

    from .events import StudioEvent
    from .storage import load_cached_events
except ImportError:
    import user_config
    from user_config import Settings

    from _vendor.icalevents import icalevents

    from events import StudioEvent
    from storage import load_cached_events


def export(month: int = datetime.now().month, year: int = datetime.now().year):
    settings = Settings()

    events = fetch_events(year, month, settings)

    parsed_events = parse_events(events, settings)
    combined_events = combine_adjacent_events(parsed_events)

    event_list_string = ''
    for event in combined_events:
        event_list_string = event_list_string + event.__str__([]) + '\n'

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


def fetch_events(year: int, month: int, settings: Settings):
    cal = calendar.Calendar()
    month_dates_nearby = cal.itermonthdates(year, month)
    month_dates = []

    for date in month_dates_nearby:
        if date.month == month:
            month_dates.append(date)

    calendar_url = settings.calendar_url
    events = icalevents.events(url=calendar_url, fix_apple=True, start=month_dates[0], end=month_dates[-1])
    return events


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


def parse_events(events: list[icalevents.Event], settings: Settings) -> list[StudioEvent]:
    parsed_events = []

    for ical_event in events:
        studio_event = _parse_event(ical_event, settings)
        parsed_events.append(studio_event)

    return parsed_events
