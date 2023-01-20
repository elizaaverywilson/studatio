import pytest
import os
from pathlib import Path

# See https://youtrack.jetbrains.com/issue/PY-53913/ModuleNotFoundError-No-module-named-pydevtestspython
from .conftest import patch_config_dir
# noinspection PyProtectedMember
from studatio.user_config import Settings, set_config_path, CONFIG_DIR, _CONFIG_DIR_VAR


def test_create_new_config():
    def example_url(_):
        return 'https://examplecalendar.com'

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        settings = Settings()
        assert settings._parse_config() == settings._default_config()


def test_empty_url_error():
    def empty_url(_):
        return ''

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', empty_url)
        with pytest.raises(ValueError):
            Settings()


def test_reset_config_dir_env_var(tmp_path):
    # Clears the config dir env var so that initiating an instance of Settings will set the env var to the default path.
    set_config_path(None)

    def example_url(_) -> str:
        return 'example.com'

    def pass_func(*_):
        pass

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('builtins.input', example_url)
        mp.setattr('os.mkdir', pass_func)
        mp.setattr('studatio.user_config.Settings._create_new_config', pass_func)
        mp.setattr('studatio.user_config.Settings._parse_config', pass_func)
        mp.setattr('studatio.user_config.Settings._read_config', pass_func)
        Settings()

    assert Path(os.environ.get(_CONFIG_DIR_VAR)) == CONFIG_DIR

    patch_config_dir(tmp_path)
