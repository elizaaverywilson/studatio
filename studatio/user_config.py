import os
from pathlib import Path

import tomlkit

try:
    from .cfg import CONFIG_DIR
except ImportError:
    from cfg import CONFIG_DIR

_CONFIG_DIR_VAR = 'STUDATIO_CONFIG'


def set_config_path(config_dir: Path = CONFIG_DIR):
    os.environ[_CONFIG_DIR_VAR] = str(config_dir)


class Settings:
    def __init__(self, config: tomlkit.document() = None, use_config_dir: bool = True):
        if use_config_dir is False:
            if config is None:
                config = self._default_config()
        else:
            if os.environ.get(_CONFIG_DIR_VAR) == 'None' or os.environ.get(_CONFIG_DIR_VAR) is None:
                set_config_path()

            _config_dir = Path(os.environ.get(_CONFIG_DIR_VAR))

            if not _config_dir.exists():
                os.mkdir(_config_dir)

            self.config_path = _config_dir / 'config.toml'

            if not self.config_path.exists():
                self._create_new_config()

            config = self._parse_config()
        # noinspection PyTypeChecker
        self._read_config(config)

    def _read_config(self, config: tomlkit.document()):
        self.calendar_url: str = config['calendar_url']
        self.instruments: set[str] = config['instruments']
        self.event_types: list[str] = config['event_types']

    def _parse_config(self) -> tomlkit.document():
        with open(self.config_path) as c:
            config_str = c.read()
        return tomlkit.parse(config_str)

    def _set_calendar_url(self):
        url = input('Calendar URL:')

        if url == '':
            raise ValueError('URL cannot be empty!')
        self.calendar_url = url

    def _default_config(self) -> tomlkit.document():
        config = tomlkit.document()
        config.add('title', 'studatio Configuration')
        self._set_calendar_url()
        config.add('calendar_url', self.calendar_url)
        config.add('instruments', ['Violin', 'Viola', 'Fiddle'])
        config.add('event_types', ['Trial Lesson', 'Lesson', 'Class Performance', 'Class', 'Dress Recital', 'Recital'])

        return config

    def _write_config(self, config: tomlkit.document()):
        with open(self.config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

    def _create_new_config(self):
        self._write_config(self._default_config())
