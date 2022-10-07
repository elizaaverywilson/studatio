from datetime import datetime
import pickle

import pytest

from studatio.storage import cache_events, load_cached_events
from studatio.events import StudioEvent


@pytest.fixture
def events():
    event1 = StudioEvent(datetime(2021, 9, 3, 1), datetime(2021, 9, 3, 2))
    event2 = StudioEvent(datetime(2022, 10, 3, 2), datetime(2022, 10, 3, 3))
    return [event1, event2]


def test_cache_events(events, tmp_path):
    path = tmp_path / 'events.cache'
    cache_events(events, path)
    assert events == load_cached_events(path)
