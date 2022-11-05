from datetime import timedelta

import pytest
from hypothesis import given, reject
from hypothesis.strategies import datetimes, timedeltas, lists, tuples

from studatio.storage import cache_events, load_cached_events
from studatio.events import StudioEvent


@pytest.fixture(scope='session')
def cache_path(tmp_path_factory):
    return tmp_path_factory.mktemp('cache').joinpath('events.cache')


@given(event_times=lists(tuples(datetimes(),
                                timedeltas(min_value=timedelta(), max_value=timedelta(seconds=10000))), max_size=100))
def test_cache_events(event_times, cache_path):
    events = []
    try:
        for times in event_times:
            events += [StudioEvent(times[0], times[0] + times[1])]
    except NotImplementedError:
        reject()

    cache_events(events, cache_path)
    assert events == load_cached_events(cache_path)
