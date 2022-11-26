import datetime

import pytest
import hypothesis.strategies as st

from studatio.user_config import set_config_path
from studatio.cal_handler import MonthYear


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.delattr('httplib2.Http.request')


def patch_config_dir(tmp_path):
    set_config_path(tmp_path / '.config')


@pytest.fixture(autouse=True)
def patch_config_dir_fixture(tmp_path):
    patch_config_dir(tmp_path)


@pytest.fixture(scope='session')
def config_dir_path(tmp_path_factory):
    return tmp_path_factory.mktemp('config')


@st.composite
def st_example_urls(draw):
    return draw(st.text(min_size=1))


@st.composite
def st_month_years(draw):
    month = draw(st.integers(min_value=1, max_value=12))
    # year max_value must be below MAXYEAR, because calendar.itermonth may return dates one year higher.
    year = draw(st.integers(min_value=datetime.MINYEAR, max_value=datetime.MAXYEAR - 1))
    return MonthYear(month, year)
