import calendar
from datetime import datetime

try:
    # For running via CLI
    from . import config_handler
    from .config_handler import Settings

    from ._vendor.icalevents import icalevents

    from .enums import StudioEventType, Instrument
    from .events import StudioEvent
except ImportError:
    import config_handler
    from config_handler import Settings

    from _vendor.icalevents import icalevents

    from enums import StudioEventType, Instrument
    from events import StudioEvent


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
    config_str = config_handler.read_config(settings)
    if not config_str:
        config_handler.new_config(settings)

    should_rewrite_config = settings.setup(config_str)
    if should_rewrite_config is True:
        config_handler.write_config(settings)

    calendar_url = settings.calendar_url
    events = icalevents.events(url=calendar_url, fix_apple=True, start=month_dates[0], end=month_dates[-1])
    return events


def parse_events(events):
    parsed_events = []

    for event in events:
        start_time = event.start
        end_time = event.end
        if 'Trial Lesson' in event.summary:
            kind = StudioEventType.TRIAL_LESSON
        elif 'Lesson' in event.summary:
            kind = StudioEventType.LESSON
        elif 'Class Performance' in event.summary:
            kind = StudioEventType.CLASS_PERFORMANCE
        elif 'Class' in event.summary:
            kind = StudioEventType.CLASS
        elif 'Dress Recital' in event.summary:
            kind = StudioEventType.DRESS_RECITAL
        elif 'Recital' in event.summary:
            kind = StudioEventType.RECITAL
        else:
            print('Alert: OTHER event type')
            kind = StudioEventType.OTHER

        instruments = set()
        if 'Violin' in event.summary:
            instruments.add(Instrument.VIOLIN)
        if 'Viola' in event.summary:
            instruments.add(Instrument.VIOLA)
        if 'Fiddle' in event.summary:
            instruments.add(Instrument.FIDDLE)

        studio_event = StudioEvent(start_time, end_time, kind, instruments)
        parsed_events.append(studio_event)

    return parsed_events
