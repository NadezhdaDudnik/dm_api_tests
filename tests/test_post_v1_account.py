import time

from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    api = Facade(host='http://localhost:5051')
    login = "login36"
    email = "login36@mail.ru"
    password = "login_55"
    db = DmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
    db.delete_user_by_login(login=login)
    dataset = db.get_user_by_login(login=login)
    assert len(dataset) == 0
    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} is not registered'
        assert row['Activated'] is False, f'User {login} is was activated'

    db.update_user_activated(login=login)
    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Activated'] is True, f'User {login} is not activated'

    time.sleep(2)

    api.account.activate_registered_user(login=login)
    for row in dataset:
        assert row['Activated'] is True, f'User {login} is activated yet'

    dataset = db.get_user_by_login(login=login)
    time.sleep(2)

    for row in dataset:
        assert row['Activated'] is True, f'User {login} is not activated'

    api.login.login_user(login=login, password=password)

    # token = api.login.get_auth_token(login='login27', password='login_55')
    # api.account.set_headers(headers=token)
    # api.login.set_headers(headers=token)
    # api.login_api.delete_v1_account_login()
    # api.account.get_current_user_info()
    # api.login.logout_user_from_all_devices()
