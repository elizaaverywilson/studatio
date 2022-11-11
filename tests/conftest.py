import pytest
import hypothesis.strategies as st


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.delattr('httplib2.Http.request')


@st.composite
def st_example_url(draw):
    return draw(st.text(min_size=1))
