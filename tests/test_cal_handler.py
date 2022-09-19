import datetime

from enums import Instrument
import cal_handler
from events import StudioEvent


class TestCombine:
    start = datetime.datetime(2021, 9, 3)
    delta = datetime.timedelta(hours=1)
    event1 = StudioEvent(start_time=start, end_time=start+delta, instruments={Instrument.FIDDLE})
    event2 = StudioEvent(start_time=start+delta, end_time=start+2*delta, instruments={Instrument.VIOLA})
    event3 = StudioEvent(start_time=start+4*delta, end_time=start+5*delta, instruments={Instrument.VIOLIN})

    combined_events = cal_handler.combine_adjacent_events([event1, event2, event3])

    def test_length(self):
        assert len(self.combined_events) == 2

    def test_start_time(self):
        assert self.combined_events[0].start_time == self.start
        assert self.combined_events[1].start_time == self.start+4*self.delta

    def test_end_time(self):
        assert self.combined_events[0].end_time == self.start+2*self.delta
        assert self.combined_events[1].end_time == self.start+5*self.delta

    def test_insrruments(self):
        assert self.combined_events[0].instruments == {Instrument.FIDDLE, Instrument.VIOLA}
        assert self.combined_events[1].instruments == {Instrument.VIOLIN}

    def test_plural(self):
        assert self.combined_events[0].plural is True
        assert self.combined_events[1].plural is False
