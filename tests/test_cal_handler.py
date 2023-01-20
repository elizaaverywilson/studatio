import datetime
from zoneinfo import ZoneInfo

import pytest
from _pytest.monkeypatch import MonkeyPatch
import hypothesis as hyp
import hypothesis.strategies as st
import icalevents.icalevents as icalevents

from studatio import cal_handler
from studatio.events import StudioEvent, MonthYear
from studatio.user_config import Settings

try:
    from strategies import st_example_urls, st_month_years, st_hours, st_minutes, st_studio_events
except ImportError or ModuleNotFoundError:
    from .strategies import st_example_urls, st_month_years, st_hours, st_minutes, st_studio_events


@hyp.given(month_year=st_month_years())
def test_check_month_years(month_year):
    assert month_year


@hyp.given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_month(month, year):
    hyp.assume(month not in range(1, 13))
    with pytest.raises(ValueError):
        MonthYear(month=month, year=year)


@hyp.given(month=st.integers(), year=st.integers())
def test_raises_error_for_invalid_year(month, year):
    hyp.assume(year not in range(datetime.MINYEAR, datetime.MAXYEAR))
    with pytest.raises(ValueError):
        MonthYear(month=month, year=year)


@hyp.settings(max_examples=50)
@hyp.given(dates_list=st.lists(st.dates()), events=st.lists(st_studio_events()), url=st_example_urls())
def test_export_schedule(dates_list, events, url):
    month_years = []

    for date in dates_list:
        month_years.append(MonthYear(month=date.month, year=date.year))

    def mocked_events(*_):
        return events

    def example_url(_):
        return url

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler._fetch_parsed', mocked_events)
        mp.setattr('builtins.input', example_url)
        cal_handler.export_schedule(month_years, Settings())


@hyp.settings(max_examples=50)
@hyp.given(dates_list=st.lists(st.dates()), events=st.lists(st_studio_events()), url=st_example_urls(), data=st.data())
def test_elapsed_in_months(dates_list, events, url, data):
    month_years = []

    for date in dates_list:
        month_years.append(MonthYear(month=date.month, year=date.year))

    def mocked_events(a_month_year, *_):
        events_to_return = []

        for an_event in events:
            if event.month_year == a_month_year:
                events_to_return += an_event
        return events_to_return

    def example_url(_):
        return url

    expected_delta_sum = datetime.timedelta(0)

    for event in events:
        # We are only looking at events that fall under a month_year in month_years, so let us remove other dates
        is_event_in_month_years = False
        for month_year in month_years:
            if event.start_time.month == month_year.month and event.start_time.year == month_year.year:
                is_event_in_month_years = True
                break

        if is_event_in_month_years:
            delta = data.draw(st.timedeltas(min_value=datetime.timedelta(minutes=1),
                                            max_value=datetime.timedelta(hours=6)))
            try:
                event.end_time = event.start_time + delta
            except NotImplementedError:
                delta = event.end_time - event.start_time
            expected_delta_sum += delta
            hyp.note('Delta sum' + str(expected_delta_sum))

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler._fetch_parsed', mocked_events)
        mp.setattr('builtins.input', example_url)

        output_delta_sum = cal_handler.elapsed_in_months(month_years, Settings())
        assert output_delta_sum == expected_delta_sum


@hyp.given(events=st.lists(st_studio_events()), data=st.data())
def test_add_elasped_from_events(events, data):
    delta_sum = datetime.timedelta(0)

    for event in events:
        delta = data.draw(st.timedeltas(min_value=datetime.timedelta(0), max_value=datetime.timedelta(hours=6)))
        try:
            event.end_time = event.start_time + delta
        except NotImplementedError:
            delta = event.end_time - event.start_time
        delta_sum += delta

    assert cal_handler._add_elapsed_from_events(events) == delta_sum


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


@hyp.given(hours=st_hours(), minutes=st_minutes())
def test_format_hours_minutes(hours, minutes):
    delta = datetime.timedelta(hours=hours, minutes=minutes)
    hours_minutes = cal_handler.format_hours_minutes(delta)
    assert hours_minutes[0] == hours
    assert hours_minutes[1] == minutes


@hyp.given(month_year=st_month_years())
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


@hyp.settings(suppress_health_check=[hyp.HealthCheck.function_scoped_fixture], max_examples=15)
# We can suppress here because event_str does not need to be reset between tests, and since shared_datadir is from a
# pytest plugin we can not change the scope.
@hyp.given(a_url=st_example_urls())
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
        month_year = MonthYear(10, 2022)
        parsed_events = cal_handler._fetch_parsed(month_year, settings)

        for event in parsed_events:
            assert event.instruments == {'Violin'}
            assert event.event_type == 'Lesson'

        assert parsed_events[0].start_time == datetime.datetime(2022, 10, 5, 12, tzinfo=ZoneInfo('America/Chicago'))
