from pathlib import Path

import appdirs
import tomlkit


class _Metadata:
    def __init__(self):
        with open('../pyproject.toml') as f:
            pyproject = f.read()
        self.metadata = tomlkit.parse(pyproject)
        self.package_name = str(self.metadata['tool']['poetry']['name'])
        self.author = str(self.metadata['tool']['poetry']['authors'][0])


_meta = _Metadata()

PACKAGE_NAME = str(_meta.package_name)
AUTHOR = str(_meta.author)
CONFIG_DIR = Path(appdirs.user_config_dir(PACKAGE_NAME, AUTHOR))
DATA_DIR = Path(appdirs.user_data_dir(PACKAGE_NAME, AUTHOR))
CACHE_DIR = Path(appdirs.user_cache_dir(PACKAGE_NAME, AUTHOR))
