import pytest


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.delattr('httplib2.Http.request')
