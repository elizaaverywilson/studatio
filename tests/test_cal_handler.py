import datetime
from zoneinfo import ZoneInfo

import pytest
from _pytest.monkeypatch import MonkeyPatch
from hypothesis import given, reject, assume
import hypothesis.strategies as st

# Needs to be changed when icalevents is no longer vendorized
from studatio.cal_handler import icalevents

from studatio import cal_handler
from studatio.events import StudioEvent
from studatio.user_config import Settings


@given(month=st.integers(min_value=1, max_value=12),
       year=st.integers(min_value=datetime.MINYEAR, max_value=datetime.MAXYEAR))
def test_check_month_years(month, year):
    cal_handler.MonthYear(month=month, year=year)


@given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_month(month, year):
    assume(month not in range(1, 13))
    with pytest.raises(ValueError):
        cal_handler.MonthYear(month=month, year=year)


@given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_year(month, year):
    assume(year not in range(datetime.MINYEAR, datetime.MAXYEAR))
    with pytest.raises(ValueError):
        cal_handler.MonthYear(month=month, year=year)


@pytest.fixture(scope='session')
def config_dir_path(tmp_path_factory):
    return tmp_path_factory.mktemp('config')


@given(dates_list=st.lists(st.dates()), event_times=st.lists(st.datetimes()))
def test_export_schedule(dates_list: [datetime.date], event_times, config_dir_path):
    events = []
    for event_time in event_times:
        try:
            events.append(StudioEvent(start_time=event_time))
        except NotImplementedError:
            reject()

    month_years = []

    for date in dates_list:
        month_years.append(cal_handler.MonthYear(month=date.month, year=date.year))

    # noinspection PyUnusedLocal
    def mocked_events(month_year, settings):
        return events

    # noinspection PyUnusedLocal
    def example_url(string=''):
        return 'https://example.com'

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler._fetch_parsed', mocked_events)
        mp.setattr('builtins.input', example_url)
        cal_handler.export_schedule(month_years, Settings(config_dir=config_dir_path))


def make_combined_events(start, delta):
    event1 = StudioEvent(start_time=start, end_time=start + delta, instruments={'Fiddle'})
    event2 = StudioEvent(start_time=start + delta, end_time=start + 2 * delta, instruments={'Viola'})
    event3 = StudioEvent(start_time=start + 4 * delta, end_time=start + 5 * delta, instruments={'Violin'})

    # noinspection PyProtectedMember
    return cal_handler._combine_adjacent_events([event1, event2, event3])


@given(start=st.datetimes(), delta=st.timedeltas(min_value=datetime.timedelta(),
                                                 max_value=datetime.timedelta(seconds=10000)))
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
    parsed_events = cal_handler._parse_events(events_to_parse, settings)
    for event in parsed_events:
        assert event.instruments == {'Violin'}
        assert event.event_type == 'Lesson'

    assert parsed_events[0].start_time == datetime.datetime(2022, 10, 5, 12, tzinfo=ZoneInfo('America/Chicago'))
