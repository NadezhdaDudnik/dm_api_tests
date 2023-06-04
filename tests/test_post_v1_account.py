import time

import pytest
from hamcrest import assert_that, has_entries
from generic.helpers.orm_models import User
from collections import namedtuple
from string import ascii_letters, digits
import random


def random_string(begin=1, end=10):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(symbols)
    return string


class TestsPostV1Account:

    @pytest.fixture
    def prepare_user(self, dm_api_facade, dm_orm):
        user = namedtuple('User', 'login, email, password, status_code')
        User = user(login="login42", email="login42@mail.ru", password="login_55", status_code=201)
        dm_orm.delete_user_by_login(login=User.login)
        dataset = dm_orm.get_user_by_login(login=User.login)
        assert len(dataset) == 0
        dm_api_facade.mailhog.delete_all_messages()
        return User

    def test_post_v1_account(self, dm_api_facade, dm_orm, prepare_user):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        status_code = prepare_user.status_code
        dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        dataset = dm_orm.get_user_by_login(login=login)
        row: User
        for row in dataset:
            assert_that(row, has_entries(
                {
                    'Login': login,
                    'Activated': False
                }
            ))

        dm_orm.update_user_activated(login=login)
        dataset = dm_orm.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True, f'User {login} is not activated'

        time.sleep(2)

        dm_api_facade.account.activate_registered_user(login=login)
        for row in dataset:
            assert row.Activated is True, f'User {login} is activated yet'

        dataset = dm_orm.get_user_by_login(login=login)
        time.sleep(2)

        for row in dataset:
            assert row.Activated is True, f'User {login} is not activated'

        dm_api_facade.login.login_user(login=login, password=password)

    '''@pytest.mark.parametrize('login, email, password', [
        ('login43', 'login43@mail.ru', 'login_55'),
        ('login', 'login@mail.ru', 'login'),
        ('465464663', '554546@mail.ru', '4566456655'),
        ('#$%%%%%%%%%%%', '#####%%@mail.ru', '$#%%#%%%%'),
    ])'''

    @pytest.mark.parametrize('login', [random_string(1, 7) for _ in range(3)])
    @pytest.mark.parametrize('email', [random_string(1, 7) + '@' + random_string(5, 5) + '.ru' for _ in range(3)])
    @pytest.mark.parametrize('password', [random_string(1, 7) for _ in range(3)])
    @pytest.mark.parametrize('status_code', [400 for _ in range(3)])
    def test_create_and_activate_user(self, dm_api_facade, dm_orm, login, email, password, status_code, assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        assertions.check_user_was_created(login=login)
        # dm_api_facade.account.activate_registered_user(login=login)
        assertions.check_user_update_activation(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @pytest.mark.parametrize('login, email, password, status_code, check_error', [
        ('login_51', 'login_51@mail.ru', 'login_55', 201, ''),
        ('login_47', 'login_47233@mail.ru', 'login', 400, {"Password": ['Short']}),
        ('l', 'login_47222@mail.ru', 'login_55', 400, {"Login": ['Taken']}),
        ('login_47', '@mail.ru', 'login_55', 400, {"Email": ['Invalid']}),
        ('login_47', 'login_47mail.ru', 'login_55', 400, {"Email": ['Invalid']}),
    ])
    def test_create_and_activated_user_with_random_params(self, dm_api_facade, dm_orm, login, email, password,
                                                          status_code,
                                                          check_error):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        response = dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        if status_code == 201:
            dataset = dm_orm.get_user_by_login(login=login)
            row: User
            for row in dataset:
                assert_that(row, has_entries(
                    {
                        'Login': login,
                        'Activated': False
                    }
                ))
            dm_orm.update_user_activated(login=login)
            dataset = dm_orm.get_user_by_login(login=login)
            for row in dataset:
                assert row.Activated is True, f'User {login} is not activated'

            time.sleep(2)

            dm_api_facade.account.activate_registered_user(login=login)
            for row in dataset:
                assert row.Activated is True, f'User {login} is activated yet'

            dataset = dm_orm.get_user_by_login(login=login)
            time.sleep(2)

            for row in dataset:
                assert row.Activated is True, f'User {login} is not activated'

            dm_api_facade.login.login_user(login=login, password=password)
        elif status_code != 201 and check_error == "Taken":
            print(check_error)
            assert_that(response.json()['errors'], has_entries(
                check_error
            ))
        elif status_code != 201 and check_error == "Invalid":
            print(check_error)
            assert_that(response.json()['errors'], has_entries(
                check_error
            ))
        elif status_code != 201 and check_error == "Short":
            print(check_error)
            assert_that(response.json()['errors'], has_entries(
                check_error
            ))

        '''db = DmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
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
    
        db.update_user_activated(login=login, is_activated=is_activated)
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
        '''

        # token = api.login.get_auth_token(login='login27', password='login_55')
        # api.account.set_headers(headers=token)
        # api.login.set_headers(headers=token)
        # api.login_api.delete_v1_account_login()
        # api.account.get_current_user_info()
        # api.login.logout_user_from_all_devices()
