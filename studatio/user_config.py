import os

import tomlkit

try:
    from .cfg import CONFIG_DIR
except ImportError:
    from cfg import CONFIG_DIR


class Settings:
    def __init__(self):
        if not CONFIG_DIR.exists():
            os.mkdir(CONFIG_DIR)

        self.config_path = CONFIG_DIR / 'config.toml'

        if not self.config_path.exists():
            self._create_new_config()

        config = self._read_config()
        self.calendar_url = config['calendar']['calendar_URL']

    def _read_config(self) -> tomlkit.document():
        with open(self.config_path) as c:
            config_str = c.read()
        return tomlkit.parse(config_str)

    def _create_new_config(self):
        def _default_config() -> tomlkit.document():
            config = tomlkit.document()
            config.add('title', 'studatio Configuration')

            calendar = tomlkit.table()
            calendar_url = input('Calendar URL:')
            calendar.add('calendar_URL', calendar_url)
            config.add('calendar', calendar)

            return config

        def _write_config(path, config):
            with open(path, 'w') as file:
                config = tomlkit.dumps(config)
                file.write(config)

        _write_config(self.config_path, _default_config())
