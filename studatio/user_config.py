import os

import tomlkit

try:
    from .cfg import CONFIG_DIR
except ImportError:
    from cfg import CONFIG_DIR


class Settings:
    def __init__(self, config_dir=CONFIG_DIR, config=None):
        if config_dir is None:
            if config is None:
                config = self._default_config()
        else:
            if not config_dir.exists():
                os.mkdir(config_dir)

            self.config_path = config_dir / 'config.toml'

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

    # noinspection PyMethodMayBeStatic
    def _set_calendar_url(self):
        return input('Calendar URL:')

    def _default_config(self) -> tomlkit.document():
        config = tomlkit.document()
        config.add('title', 'studatio Configuration')
        config.add('calendar_url', self._set_calendar_url())
        config.add('instruments', ['Violin', 'Viola', 'Fiddle'])
        config.add('event_types', ['Trial Lesson', 'Lesson', 'Class Performance', 'Class', 'Dress Recital', 'Recital'])

        return config

    def _write_config(self, config):
        with open(self.config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

    def _create_new_config(self):
        self._write_config(self._default_config())
