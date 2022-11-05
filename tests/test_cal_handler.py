import datetime
from zoneinfo import ZoneInfo

import pytest

from hypothesis import given, reject
from hypothesis.strategies import datetimes, timedeltas

# Needs to be changed when icalevents is no longer vendorized
from studatio.cal_handler import icalevents

from studatio import cal_handler
from studatio.events import StudioEvent
from studatio.user_config import Settings


def make_combined_events(start, delta):
    event1 = StudioEvent(start_time=start, end_time=start + delta, instruments={'Fiddle'})
    event2 = StudioEvent(start_time=start + delta, end_time=start + 2 * delta, instruments={'Viola'})
    event3 = StudioEvent(start_time=start + 4 * delta, end_time=start + 5 * delta, instruments={'Violin'})

    return cal_handler.combine_adjacent_events([event1, event2, event3])


@given(start=datetimes(), delta=timedeltas(min_value=datetime.timedelta(), max_value=datetime.timedelta(seconds=10000)))
def test_combined_events(start, delta):
    combined_events = None
    try:
        combined_events = make_combined_events(start, delta)
    except NotImplementedError:
        reject()

    assert len(combined_events) == 2
    assert combined_events[0].start_time == start
    assert combined_events[1].start_time == start + 4 * delta
    assert combined_events[0].end_time == start + 2 * delta
    assert combined_events[1].end_time == start + 5 * delta
    assert combined_events[0].instruments == {'Viola', 'Fiddle'}
    assert combined_events[1].instruments == {'Violin'}
    assert combined_events[0].plural is True
    assert combined_events[1].plural is False


@pytest.fixture
def events_to_parse(shared_datadir) -> list[icalevents.Event]:
    path = (shared_datadir / 'events.ical')
    downloader = icalevents.ICalDownload()
    data_str = downloader.data_from_file(path, True)
    return icalevents.parse_events(data_str, datetime.datetime(2022, 10, 1), datetime.datetime(2022, 11, 1))


def test_parse_events(events_to_parse, monkeypatch):
    monkeypatch.setattr('studatio.user_config.Settings._set_calendar_url', lambda _: 'calendar.test')
    settings = Settings(config_dir=None)
    parsed_events = cal_handler.parse_events(events_to_parse, settings)
    for event in parsed_events:
        assert event.instruments == {'Violin'}
        assert event.event_type == 'Lesson'

    assert parsed_events[0].start_time == datetime.datetime(2022, 10, 5, 12, tzinfo=ZoneInfo('America/Chicago'))
