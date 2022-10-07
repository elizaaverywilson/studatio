import pickle

import appdirs

_default_cache_path = appdirs.user_cache_dir() + 'events.cache'


def cache_events(events, path=_default_cache_path):
    with open(path, 'wb') as f:
        pickle.dump(events, f)


def load_cached_events(path=_default_cache_path):
    with open(path, 'rb') as f:
        return pickle.load(f)
