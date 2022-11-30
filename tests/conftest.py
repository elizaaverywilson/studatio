import pytest

from studatio.user_config import set_config_path


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.delattr('httplib2.Http.request')


def patch_config_dir(tmp_path):
    set_config_path(tmp_path / '.config')


@pytest.fixture(autouse=True)
def patch_config_dir_fixture(tmp_path):
    patch_config_dir(tmp_path)


@pytest.fixture(scope='session')
def config_dir_path(tmp_path_factory):
    return tmp_path_factory.mktemp('config')
