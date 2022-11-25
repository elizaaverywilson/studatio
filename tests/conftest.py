import datetime

import pytest
import hypothesis.strategies as st

from studatio.user_config import set_config_path
from studatio.cal_handler import MonthYear


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.delattr('httplib2.Http.request')


@pytest.fixture(autouse=True)
def config_dir(tmp_path):
    set_config_path(tmp_path / '.config')


@pytest.fixture(scope='session')
def config_dir_path(tmp_path_factory):
    return tmp_path_factory.mktemp('config')


@st.composite
def st_example_url(draw):
    return draw(st.text(min_size=1))


@st.composite
def st_month_year(draw):
    month = draw(st.integers(min_value=1, max_value=12))
    # year max_value must be below MAXYEAR, because calendar.itermonth may return dates one year higher.
    year = draw(st.integers(min_value=datetime.MINYEAR, max_value=datetime.MAXYEAR - 1))
    return MonthYear(month, year)
