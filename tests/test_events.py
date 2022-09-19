import datetime

from enums import Instrument, StudioEventType
from events import StudioEvent

start, end = datetime.datetime(2007, 2, 5, 3, 10, 0), datetime.datetime(2007, 2, 5, 4, 10, 0)


class TestSimpleEvent():
    event = StudioEvent(start, end, StudioEventType.LESSON, {Instrument.VIOLA})

    def test_date(self):
        assert 'Feb 05 2007' in str(self.event)

    def test_times(self):
        assert '03:10 AM to 04:10 AM' in str(self.event)

    def test_type(self):
        assert 'Lesson' in str(self.event)

    def test_instrument(self):
        assert 'Viola' in str(self.event)


class TestMultiple():
    event = StudioEvent(start, end, StudioEventType.LESSON, {Instrument.VIOLIN, Instrument.VIOLA, Instrument.FIDDLE},
                        True)

    def test_multiple_instruments(self):
        assert 'Violin/Viola/Fiddle' in str(self.event)

    def test_plural(self):
        assert 'Lessons' in str(self.event)
