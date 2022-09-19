import datetime

from enums import StudioEventType


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
