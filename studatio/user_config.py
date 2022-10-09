import os

import tomlkit

try:
    from .cfg import CONFIG_DIR
except ImportError:
    from cfg import CONFIG_DIR


class Settings:
    def __init__(self, config_dir=CONFIG_DIR):
        if not config_dir.exists():
            os.mkdir(config_dir)

        self.config_path = config_dir / 'config.toml'

        if not self.config_path.exists():
            self._create_new_config()

        config = self._read_config()
        self.calendar_url = config['calendar']['calendar_URL']

    def _read_config(self) -> tomlkit.document():
        with open(self.config_path) as c:
            config_str = c.read()
        return tomlkit.parse(config_str)

    def _set_calendar_url(self):
        self.calendar_url = input('Calendar URL:')

    def _default_config(self) -> tomlkit.document():
        config = tomlkit.document()
        config.add('title', 'studatio Configuration')

        calendar = tomlkit.table()
        calendar.add('calendar_URL', self._set_calendar_url())
        config.add('calendar', calendar)

        return config

    def _write_config(self, config):
        with open(self.config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

    def _create_new_config(self):
        self._write_config(self._default_config())
