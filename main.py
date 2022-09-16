from datetime import datetime
import sys
import calendar
from enum import Enum, auto

from icalevents import icalevents
import pyperclip


# TODO Make recurring task
# TODO Auto Update


def export(month: int = datetime.now().month, year: int = datetime.now().year):
    events = fetch_events(year, month)
    events.sort()
    parsed_events = parse_events(events)
    combine_adjecent_events(parsed_events)

    event_list_string = ''
    for event in parsed_events:
        event_list_string = event_list_string + str(event) + '\n'

    return event_list_string


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name.capitalize()


class StudioEventType(AutoName):
    LESSON = auto()
    CLASS = auto()
    CLASS_PERFORMANCE = auto()
    RECITAL = auto()
    DRESS_RECITAL = auto()
    OTHER = auto()


class Instrument(AutoName):
    VIOLIN = auto()
    FIDDLE = auto()
    VIOLA = auto()


class StudioEvent:
    def __init__(self, start_time: datetime, end_time: datetime, kind: StudioEventType, instruments: set, plural=False):
        if start_time.date == end_time.date:
            raise ValueError('Multi-day events?')
        self.start_time = start_time
        self.end_time = end_time
        self.kind = kind
        self.instruments = instruments
        self.plural = plural

    def date(self):
        return self.start_time.date()

    def __str__(self):
        if self.plural is True:
            if self.kind is not StudioEventType.LESSON:
                raise NotImplementedError('Unsupported plural event type.')
            else:
                pl = 's'
        else:
            pl = ''
        instr = ''
        if len(self.instruments) >= 1:
            i = 1
            for instrument in self.instruments:
                if i == 1:
                    instr = str(instrument)
                else:
                    instr += '/' + str(instrument)
                i += 1
            instr += ' '
        time_format = '%I:%M %p'
        return self.date().strftime('%b %d %Y ') + \
               instr + \
               str(self.kind) + pl + ' ' + \
               self.start_time.time().strftime(time_format) + ' to ' + \
               self.end_time.time().strftime(time_format)


def combine_adjecent_events(events: list):
    for event in events:
        try:
            # noinspection PyUnboundLocalVariable
            previous_event
        except NameError:
            previous_event = event
        else:
            if previous_event.end_time == event.start_time and previous_event.kind == event.kind:
                events.remove(previous_event)
                combined_instruments = previous_event.instruments.union(event.instruments)
                combined_event = StudioEvent(start_time=previous_event.start_time,
                                             end_time=event.end_time,
                                             kind=event.kind,
                                             instruments=combined_instruments,
                                             plural=True)

                i = events.index(event)
                events.insert(i, combined_event)
                events.remove(event)

            previous_event = event


def fetch_events(year: int, month: int):
    cal = calendar.Calendar()
    month_dates_nearby = cal.itermonthdates(year, month)
    month_dates = []

    for date in month_dates_nearby:
        if date.month == month:
            month_dates.append(date)

    url = 'webcal://p30-caldav.icloud.com/published/2/MTk2MDQ1NTIxMTE5NjA0NW3qWjWWh8nVD_plyRieYX3OLKe0JldG7dI5' \
          'LpuI06N5veSvp9Cabs3A3_XwEIJ-UR1-jQ9ql2SNSPfTd2ZEB_I'
    events = icalevents.events(url=url, fix_apple=True, start=month_dates[0], end=month_dates[-1])
    return events


def parse_events(events):
    parsed_events = []

    for event in events:
        start_time = event.start
        end_time = event.end
        if 'Lesson' in event.summary:
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


if __name__ == '__main__':
    if len(sys.argv) == 1:
        export_str = str(export())
    elif len(sys.argv) == 2 or len(sys.argv) == 3:
        month_str = sys.argv[1]
        try:
            int(month_str)
            months = [int(month_str)]
        except ValueError:
            monthBounds = month_str.split('-')
            months = list(range(int(monthBounds[0]), int(monthBounds[1]) + 1))
        export_str = ''
        i = 1
        for month in months:
            if i > 1:
                export_str += '\n'
            if len(sys.argv) == 2:
                export_str += str(export(month))
            else:
                export_str += str(export(month, int(sys.argv[2])))
            i += 1
    else:
        raise AttributeError()
    print(export_str)
    pyperclip.copy(export_str)
