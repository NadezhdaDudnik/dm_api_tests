import pytest
from vyper import v
from pathlib import Path

from generic.assertions.post_v1_account import AssertionsPostV1Account
from generic.helpers.mailhog import MailhogApi
from generic.helpers.orm_db import OrmDatabase
from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade
import structlog
from grpclib.client import Channel

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host=v.get('service.mailhog'))


@pytest.fixture
def dm_api_facade(mailhog):
    return Facade(host=v.get('service.dm_api_account'),
                  mailhog=mailhog
                  )


options = (
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host',
)

connect = None


@pytest.fixture
def dm_db():
    global connect
    if connect is None:
        connect = DmDatabase(
            user=v.get('database.dm3_5.user'),
            password=v.get('database.dm3_5.password'),
            host=v.get('database.dm3_5.host'),
            database=v.get('database.dm3_5.database'))
    yield connect
    connect.db.db.close()


@pytest.fixture
def dm_orm():
    orm = OrmDatabase(user=v.get('database.dm3_5.user'),
                      password=v.get('database.dm3_5.password'),
                      host=v.get('database.dm3_5.host'),
                      database=v.get('database.dm3_5.database'))
    yield orm
    orm.db.close_connection()


@pytest.fixture()
def assertions(dm_orm):
    return AssertionsPostV1Account(dm_orm)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)
