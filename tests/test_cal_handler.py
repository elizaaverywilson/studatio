import datetime

import pytest

from studatio import cal_handler
from studatio.events import StudioEvent


@pytest.fixture
def start():
    return datetime.datetime(2021, 9, 3)


@pytest.fixture
def delta():
    return datetime.timedelta(hours=1)


@pytest.fixture
def combined_events(start, delta):
    event1 = StudioEvent(start_time=start, end_time=start + delta, instruments={'Fiddle'})
    event2 = StudioEvent(start_time=start + delta, end_time=start + 2 * delta, instruments={'Viola'})
    event3 = StudioEvent(start_time=start + 4 * delta, end_time=start + 5 * delta, instruments={'Violin'})

    return cal_handler.combine_adjacent_events([event1, event2, event3])


def test_length(combined_events):
    assert len(combined_events) == 2


def test_start_time(start, delta, combined_events):
    assert combined_events[0].start_time == start
    assert combined_events[1].start_time == start + 4 * delta


def test_end_time(start, delta, combined_events):
    assert combined_events[0].end_time == start + 2 * delta
    assert combined_events[1].end_time == start + 5 * delta


def test_instruments(combined_events):
    assert combined_events[0].instruments == {'Viola', 'Fiddle'}
    assert combined_events[1].instruments == {'Violin'}


def test_plural(combined_events):
    assert combined_events[0].plural is True
    assert combined_events[1].plural is False

# @pytest.fixture
# def events_to_parse():
#    raise NotImplementedError


# def test_parse_events(events_to_parse):
#    raise NotImplementedError
