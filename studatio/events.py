import datetime
from dataclasses import dataclass
from datetime import date

try:
    pass
except ImportError:
    pass


class StudioEvent:
    def __init__(self,
                 start_time: datetime = datetime.datetime.now(),
                 end_time: datetime = None,
                 event_type: str = None,
                 instruments: set = {},
                 plural: bool = False):

        self.start_time = start_time
        if end_time is None:
            end_time = start_time + datetime.timedelta(hours=1)
        self.end_time = end_time
        if start_time.date() != end_time.date():
            error_msg = ('Multi-day events are not currently supported. start_time = %s, end_time = %s' %
                         (start_time, end_time))
            raise NotImplementedError(error_msg)

        self.event_type = event_type
        self.instruments = instruments
        self.plural = plural

    def date(self):
        return self.start_time.date()

    def month_year(self):
        month = self.date().month
        year = self.date().year
        return MonthYear(month, year)

    def __str__(self, instruments_sort_key=None):
        if self.plural is True:
            pl = 's'
        else:
            pl = ''
        instr = ''
        if len(self.instruments) >= 1:

            # convert self.instruments to a list, so we can sort it.
            instruments_list = []
            for instrument in self.instruments:
                instruments_list.append(instrument)
            if instruments_sort_key:
                instruments_list.sort(key=lambda ins: instruments_sort_key.index(ins))

            i = 1
            for instrument in instruments_list:
                if i == 1:
                    instr = str(instrument)
                else:
                    instr += '/' + str(instrument)
                i += 1
            instr += ' '

        time_format = '%I:%M %p'
        return self.date().strftime('%b %d %Y ') + \
               instr + \
               str(self.event_type) + pl + ' ' + \
               self.start_time.time().strftime(time_format) + ' to ' + \
               self.end_time.time().strftime(time_format)

    def __eq__(self, other):
        if (
                self.start_time == other.start_time
                and self.end_time == other.end_time
                and self.event_type == other.event_type
                and self.instruments == other.instruments
                and self.plural == other.plural
        ):
            return True
        else:
            return False


@dataclass(frozen=True)
class MonthYear:
    # Raises ValueError if month is not an integer from 1-12 or year is not a valid date year.
    month: int
    year: int

    def __post_init__(self):
        try:
            date(self.year, self.month, 1)
        except OverflowError:
            raise ValueError
