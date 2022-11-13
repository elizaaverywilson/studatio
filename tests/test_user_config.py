import pytest

from studatio.user_config import Settings


@pytest.fixture
def config_dir(tmp_path):
    return tmp_path / '.config'


def test_create_new_config(config_dir):
    def example_url(_):
        return 'https://examplecalendar.com'

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        settings = Settings(config_dir)
        assert settings._parse_config() == settings._default_config()


def test_empty_url_error(config_dir):
    def example_url(_):
        return ''

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        with pytest.raises(ValueError):
            Settings(config_dir)
