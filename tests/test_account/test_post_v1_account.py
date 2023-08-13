import time

import allure
import pytest
from hamcrest import assert_that, has_entries, has_properties
from collections import namedtuple
from string import ascii_letters, digits
import random
from data.post_v1_account import PostV1AccountData as user_data
from generic.assertions.response_checker import check_status_code_http


def random_string(begin=1, end=10):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(symbols)
    return string


@allure.suite("Тесты на проверку метода POST{host}/v1/account")
@allure.sub_suite("Позитивные и негативные проверки")
class TestsPostV1Account:
    random_email = f'{random_string()}@{random_string()}.{random_string()}'
    valid_login = random_string(2)
    invalid_login = random_string(1, 1)
    valid_password = random_string(6)
    invalid_password = random_string(1, 5)
    invalid_email = f'{random_string(6)}@'
    invalid_email_1 = random_string(1, 2).replace('@', '')

    random_data = [
        (valid_login, random_email, valid_password, 201, ''),
        (valid_login, random_email, invalid_password, 400, {"Password": ["Short"]}),
        (invalid_login, random_email, valid_password, 400, {"Login": ["Short"]}),
        (valid_login, invalid_email, valid_password, 400, {"Email": ["Invalid"]}),
        (valid_login, invalid_email_1, valid_password, 400, {"Email": ["Invalid"]}),
    ]

    @allure.step("Подготовка тестового пользователя")
    @pytest.fixture
    def prepare_user(self, dm_api_facade, dm_orm):
        data = namedtuple('user', 'login, email, password')
        user = data(login=user_data.login,
                    email=user_data.email,
                    password=user_data.password
                    )
        dm_orm.delete_user_by_login(login=user.login)
        dataset = dm_orm.get_user_by_login(login=user.login)
        assert len(dataset) == 0
        dm_api_facade.mailhog.delete_all_messages()
        return user

    @allure.step("Проверка регистрации, активации и авторизации пользователя")
    def test_post_v1_account(self, dm_api_facade, dm_orm, prepare_user, assertions):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password
        )
        assertions.check_user_was_created(login=login)
        dm_orm.get_user_by_login(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @allure.title("Проверка успешной регистрации и успешной активации пользователя, и авторизации пользователя")
    @pytest.mark.parametrize('login, email, password, status_code, check_error', [
        ('l0gin_75', 'login_5752@mail.ru', 'login555', 201, '')])
    def test_create_and_activated_user_201(self, dm_api_facade, dm_orm, login, email, password,
                                           status_code,
                                           check_error, assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        with check_status_code_http(expected_status_code=status_code, expected_result=check_error):
            dm_api_facade.account.register_new_user(
                login=login,
                email=email,
                password=password,
            )
        if status_code == 201:
            assertions.check_user_was_created(login=login)
            dm_api_facade.account.activate_registered_user(login=login)
            dm_orm.get_user_by_login(login=login)
            assertions.check_user_was_activated(login=login)
            dm_api_facade.login.login_user(login=login, password=password)

    @allure.title("Проверка неуспешной регистрации")
    @pytest.mark.parametrize('login, email, password, status_code, check_error', random_data)
    def test_create_and_activated_user_400_password_short(self, dm_api_facade, dm_orm, login, email, password,
                                                          status_code,
                                                          check_error, assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        with check_status_code_http(expected_status_code=status_code, expected_result=check_error):
            dm_api_facade.account.register_new_user(
                login=login,
                email=email,
                password=password
            )
        if status_code == 201:
            assertions.check_user_was_created(login=login)
            dm_api_facade.account.activate_registered_user(login=login)
            dm_orm.get_user_by_login(login=login)
            assertions.check_user_was_activated(login=login)
            dm_api_facade.login.login_user(login=login, password=password)

        """Что тут происходит, если статус код отличный от 200, то в рамках контекстного менеджера выполнится проверка сообщения и статус кода и тест пройдет.
         В случае если, метод выполнится успешно (статус код 2хх), мы зайдем в блок if и проведем дальнейшие проверки позитивного сценария."""

