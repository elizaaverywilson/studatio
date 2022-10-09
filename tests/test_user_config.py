import pytest

from studatio.user_config import Settings


@pytest.fixture
def config_dir(tmp_path):
    return tmp_path / '.config'


def test_create_new_config(config_dir, monkeypatch):
    monkeypatch.setattr('studatio.user_config.Settings._set_calendar_url', lambda _: 'calendar.test')
    settings = Settings(config_dir)
    assert settings._parse_config() == settings._default_config()
