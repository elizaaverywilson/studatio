import datetime
from zoneinfo import ZoneInfo
import pytest
from _pytest.monkeypatch import MonkeyPatch
import hypothesis as hyp
import hypothesis.strategies as st

# Needs to be changed when icalevents is no longer vendorized
from studatio.cal_handler import icalevents

from studatio import cal_handler
from studatio.events import StudioEvent
from studatio.user_config import Settings

try:
    from .conftest import st_example_url, st_month_year
except ImportError:
    from conftest import st_example_url, st_month_year


@hyp.given(month_year=st_month_year())
def test_check_month_years(month_year):
    assert month_year


@hyp.given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_month(month, year):
    hyp.assume(month not in range(1, 13))
    with pytest.raises(ValueError):
        cal_handler.MonthYear(month=month, year=year)


@hyp.given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_year(month, year):
    hyp.assume(year not in range(datetime.MINYEAR, datetime.MAXYEAR))
    with pytest.raises(ValueError):
        cal_handler.MonthYear(month=month, year=year)


@hyp.given(dates_list=st.lists(st.dates()), event_times=st.lists(st.datetimes()), url=st_example_url())
def test_export_schedule(dates_list, event_times, url):
    events = []
    for event_time in event_times:
        try:
            events.append(StudioEvent(start_time=event_time))
        except NotImplementedError:
            hyp.reject()

    month_years = []

    for date in dates_list:
        month_years.append(cal_handler.MonthYear(month=date.month, year=date.year))

    def mocked_events(*_):
        return events

    def example_url(_):
        return url

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler._fetch_parsed', mocked_events)
        mp.setattr('builtins.input', example_url)
        cal_handler.export_schedule(month_years, Settings())


def make_combined_events(start, delta):
    event1 = StudioEvent(start_time=start, end_time=start + delta, instruments={'Fiddle'})
    event2 = StudioEvent(start_time=start + delta, end_time=start + 2 * delta, instruments={'Viola'})
    event3 = StudioEvent(start_time=start + 4 * delta, end_time=start + 5 * delta, instruments={'Violin'})

    # noinspection PyProtectedMember
    return cal_handler._combine_adjacent_events([event1, event2, event3])


@hyp.given(start=st.datetimes(), delta=st.timedeltas(min_value=datetime.timedelta(),
                                                     max_value=datetime.timedelta(seconds=10000)))
def test_combined_events(start, delta):
    combined_events = None
    try:
        combined_events = make_combined_events(start, delta)
    except NotImplementedError:
        hyp.reject()

    assert len(combined_events) == 2
    assert combined_events[0].start_time == start
    assert combined_events[1].start_time == start + 4 * delta
    assert combined_events[0].end_time == start + 2 * delta
    assert combined_events[1].end_time == start + 5 * delta
    assert combined_events[0].instruments == {'Viola', 'Fiddle'}
    assert combined_events[1].instruments == {'Violin'}
    assert combined_events[0].plural is True
    assert combined_events[1].plural is False


@hyp.given(month_year=st_month_year())
def test_days_of_month(month_year):
    month_dates = cal_handler._days_of_month(month_year)

    month_previous_date = None
    for month_date in month_dates:
        assert month_date.month == month_year.month
        assert month_date.year == month_year.year
        if month_previous_date is not None:
            assert month_date.day > month_previous_date.day
        month_previous_date = month_date
    assert len(month_dates) == month_previous_date.day


@pytest.fixture
def event_str(shared_datadir) -> str:
    path = (shared_datadir / 'events.ical')
    downloader = icalevents.ICalDownload()
    data_str = downloader.data_from_file(path, True)
    return data_str


@hyp.settings(suppress_health_check=[hyp.HealthCheck.function_scoped_fixture])
# We can suppress here because event_str does not need to be reset between tests, and since shared_datadir is from a
# pytest plugin we can not change the scope.
@hyp.given(a_url=st_example_url())
def test_fetch_parsed(event_str, a_url):
    def ical_parse_mocked(
            url: str, fix_apple: bool, start: datetime.date, end: datetime.date) -> [icalevents.Event]:
        assert url == a_url
        assert fix_apple is True

        return icalevents.parse_events(event_str, start, end)

    def example_url(_) -> str:
        return a_url

    with MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        mp.setattr('studatio.cal_handler.icalevents.events', ical_parse_mocked)

        settings = Settings(use_config_dir=False)
        month_year = cal_handler.MonthYear(10, 2022)
        parsed_events = cal_handler._fetch_parsed(month_year, settings)

        for event in parsed_events:
            assert event.instruments == {'Violin'}
            assert event.event_type == 'Lesson'

        assert parsed_events[0].start_time == datetime.datetime(2022, 10, 5, 12, tzinfo=ZoneInfo('America/Chicago'))
