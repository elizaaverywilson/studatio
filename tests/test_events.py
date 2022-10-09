import datetime

import pytest

from studatio.events import StudioEvent


@pytest.fixture
def start():
    return datetime.datetime(2007, 2, 5, 3, 10, 0)


@pytest.fixture
def end():
    return datetime.datetime(2007, 2, 5, 4, 10, 0)


class TestSimpleEvent:
    @pytest.fixture
    def event(self, start, end):
        return StudioEvent(start, end, 'Lesson', {'Viola'})

    def test_date(self, event):
        assert 'Feb 05 2007' in str(event)

    def test_times(self, event):
        assert '03:10 AM to 04:10 AM' in str(event)

    def test_type(self, event):
        assert 'Lesson' in str(event)

    def test_instrument(self, event):
        assert 'Viola' in str(event)


class TestMultipleInstruments:
    @pytest.fixture
    def event(self, start, end):
        return StudioEvent(start, end, 'Lesson', {'Violin', 'Viola', 'Fiddle'}, True)

    def test_multiple_instruments(self, event):
        assert 'Violin/Viola/Fiddle' in event.__str__(instruments_sort_key=['Violin', 'Viola', 'Fiddle'])

    def test_plural(self, event):
        assert 'Lessons' in str(event)
