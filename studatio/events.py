import datetime

try:
    from .enums import StudioEventType, Instrument
except ImportError:
    from enums import StudioEventType, Instrument


class StudioEvent:
    def __init__(self, start_time: datetime = datetime.datetime.now(),
                 end_time: datetime = datetime.datetime.now(),
                 kind: StudioEventType = StudioEventType.LESSON,
                 instruments: set = None,
                 plural: object = False):
        if instruments is None:
            instruments = {Instrument.VIOLIN}
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
            if self.kind != StudioEventType.LESSON:
                raise NotImplementedError('Unsupported plural event type.')
            else:
                pl = 's'
        else:
            pl = ''
        instr = ''
        if len(self.instruments) >= 1:

            # convert self.instruments to a list, so we can sort it.
            instruments_list = []
            for instrument in self.instruments:
                instruments_list.append(instrument)
            instruments_list.sort()

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
            str(self.kind) + pl + ' ' + \
            self.start_time.time().strftime(time_format) + ' to ' + \
            self.end_time.time().strftime(time_format)
