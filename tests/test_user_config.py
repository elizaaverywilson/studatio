import pytest

from studatio.user_config import Settings


def test_create_new_config():
    def example_url(_):
        return 'https://examplecalendar.com'

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        settings = Settings()
        assert settings._parse_config() == settings._default_config()


def test_empty_url_error():
    def example_url(_):
        return ''

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        with pytest.raises(ValueError):
            Settings()
