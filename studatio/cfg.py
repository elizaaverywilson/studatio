from pathlib import Path

import appdirs

PACKAGE_NAME = 'studatio'
CONFIG_DIR = Path(appdirs.user_config_dir(PACKAGE_NAME))
DATA_DIR = Path(appdirs.user_data_dir(PACKAGE_NAME))
CACHE_DIR = Path(appdirs.user_cache_dir(PACKAGE_NAME))
