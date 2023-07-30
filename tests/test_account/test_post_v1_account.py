import time

import allure
import pytest
from hamcrest import assert_that, has_entries, has_properties
from generic.helpers.orm_models import User
from collections import namedtuple
from string import ascii_letters, digits
import random
from data.post_v1_account import PostV1AccountData as user_data


def random_string(begin=1, end=10):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(symbols)
    return string


@allure.suite("Тесты на проверку метода POST{host}/v1/account")
@allure.sub_suite("Позитивные и негативные проверки")
class TestsPostV1Account:

    @allure.step("Подготовка тестового пользователя")
    @pytest.fixture
    def prepare_user(self, dm_api_facade, dm_orm):
        user = namedtuple('User', 'login, email, password, status_code')
        User = user(login=user_data.login, email=user_data.email, password=user_data.password, status_code=201)
        dm_orm.delete_user_by_login(login=User.login)
        dataset = dm_orm.get_user_by_login(login=User.login)
        assert len(dataset) == 0
        dm_api_facade.mailhog.delete_all_messages()
        return User

    @allure.step("Проверка регистрации, активации и авторизации пользователя")
    def test_post_v1_account(self, dm_api_facade, dm_orm, prepare_user, assertions):
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
        assertions.check_user_was_created(login=login)
        dm_orm.get_user_by_login(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        # assertions.check_user_update_activation(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @allure.title("Проверка регистрации и активации пользователя - статус код 400")
    @pytest.mark.parametrize('login', [random_string(1, 1) for _ in range(1)])
    @pytest.mark.parametrize('email', [random_string(1, 7) + '@' + random_string(5, 5) + '.ru' for _ in range(1)])
    @pytest.mark.parametrize('password', [random_string(1, 7) for _ in range(1)])
    @pytest.mark.parametrize('status_code', [400 for _ in range(1)])
    @pytest.mark.parametrize('check_error', ["Short" for _ in range(1)])
    def test_create_and_activate_user(self, dm_api_facade, dm_orm, login, email, password, status_code, check_error,
                                      assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        response = dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        print(response.json().get('errors'))
        assert_that(response.json().get('errors'), has_entries(
            {"Login": [check_error]}
        ))

    @allure.title("Проверка успешной регистрации и успешной активации пользователя, и авторизации пользователя")
    @pytest.mark.parametrize('login, email, password, status_code, check_error', [
        ('login_51', 'login_512@mail.ru', 'login_55', 201, '')])
    def test_create_and_activated_user_200_ok(self, dm_api_facade, dm_orm, login, email, password,
                                              status_code,
                                              check_error):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        if status_code == 201:
            dataset = dm_orm.get_user_by_login(login=login)
            row: User
            for row in dataset:
                assert_that(row, has_properties(
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

    @pytest.mark.parametrize('login, email, password, status_code, check_error', [
        ('login_51', 'login_51@mail.ru', 'login_55', 201, ''),
        ('login_47', 'login_47233@mail.ru', 'login', 400, 'Short'),
        ('l', 'login47222@mail.ru', 'login_55', 400, 'Short'),
        ('login2345', '@mail.ru', 'login_55', 400, 'Invalid'),
        ('login789', 'login_47222mail.ru', 'login_55', 400, 'Invalid')
    ])
    def test_create_and_activated_user_with_positive_negative_cases(self, dm_api_facade, dm_orm, login, email, password,
                                                                    status_code,
                                                                    check_error, assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        response = dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )
        with allure.step("Проверка при генерации разных тестовых данных"):
            if status_code != 201 and len(password) <= 5:
                print(check_error)
                print(status_code)
                print(response.json().get('errors'))
                assert_that(response.json().get('errors'), has_entries(
                    {'Password': [check_error]}
                ))
            elif status_code != 201 and len(login) <= 1:
                print(check_error)
                print(response.json().get('errors'))
                assert_that(response.json().get('errors'), has_entries(
                    {"Login": [check_error]}
                ))
            elif status_code != 201:
                print(check_error)
                print(response.json().get('errors'))
                assert_that(response.json().get('errors'), has_entries(
                    {'Email': [check_error]}
                ))
            else:
                assertions.check_user_was_created(login=login)
                dm_api_facade.account.activate_registered_user(login=login)
                dm_orm.get_user_by_login(login=login)
                assertions.check_user_was_activated(login=login)
                dm_api_facade.login.login_user(login=login, password=password)

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
