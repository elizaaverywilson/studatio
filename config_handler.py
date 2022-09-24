import os
from pathlib import Path

import tomlkit


class Settings:
    """Wrapper for the configuration
    Should call self.setup() if settings details are needed.
    Otherwise, referencing settings attributes besides self.config_path will raise an error."""

    def __init__(self, config_path=(Path.home() / '.config/studatio/config.toml')):
        self.config_path = config_path

        # Call setup() to prepare the attribute.
        self.calendar_url = ''

    def setup(self, config):
        """Parses config. Returns True if config needs to be rewritten"""
        try:
            self.calendar_url = config['calendar']['calendar_URL']
        except tomlkit.exceptions.NonExistentKey:
            print('Not finding calendar URL in config.')
            return True
        else:
            return False


def _default_config() -> tomlkit.document():
    config = tomlkit.document()
    config.add('title', 'studatio Configuration')

    calendar = tomlkit.table()
    calendar_url = input('Calendar URL:')
    calendar.add('calendar_URL', calendar_url)
    config.add('calendar', calendar)

    return config


def read_config(settings):
    """Reads configuration file and returns it as a TOMLDocument. Returns FALSE if it does not exist."""
    try:
        with open(settings.config_path) as c:
            config_str = c.read()
        return tomlkit.parse(config_str)
    except FileNotFoundError:
        return False


def write_config(settings):
    with open(settings.config_path, 'w') as file:
        config = tomlkit.dumps(_default_config())
        file.write(config)


def new_config(settings):
    """Creates configuration file if it does not exist."""

    print('Checking for config set-up...')
    config_path = settings.config_path

    def create_parents():
        print(str(config_path.parent) + """ does not exist.
            Creating """ + str(config_path.parent) + ' ...')
        os.makedirs(config_path.parent)
        print(str(config_path.parent) + ' created.')

    if not config_path.parent.exists():
        create_parents()
    if not config_path.exists():
        print(str(config_path) + """ does not exist.
            Creating """ + config_path.name + ' ...')
        write_config(config_path)
        print(config_path.name + ' created at ' + str(config_path) + '.')
    else:
        print('Config already exists at ' + str(config_path) + '.')
