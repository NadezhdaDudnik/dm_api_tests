import json
import time

import allure
from requests import Response
from common_libs.restclient.restclient import Restclient


def decorator(fn):
    def wrapper(*args, **kwargs):
        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']
            if len(emails) < 5:
                print(f'attempt {i}')
                time.sleep(2)
                continue
            else:
                return response

    return wrapper


class MailhogApi:
    def __init__(self, host='http://localhost:5025', headers=None):
        self.host = host
        self.client = Restclient(host=host)

    # @decorator
    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        with allure.step("Получение писем"):
            response = self.client.get(
                path="/api/v2/messages",
                params={
                    'limit': limit
                }
            )

        return response

    def get_token_from_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """
        emails = self.get_api_v2_messages(limit=1).json()
        with allure.step("Получение токена по последнему письму"):
            token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
            token = token_url.split('/')[-1]
        return token

    def get_token_by_login(self, login: str, attempt=50):
        with allure.step("Получение токена из письма по Login"):
            if attempt == 0:
                raise AssertionError(f'Не удалось получить письмо с логином {login}')
            emails = self.get_api_v2_messages(limit=50).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    print(token)
                    return token
            time.sleep(2)
            print('try')
            return self.get_token_by_login(login=login, attempt=attempt - 1)

    def get_token_from_last_email_reset(self, login: str, attempt=50):
        """
        Get user reset email
        :return:
        """
        with allure.step("Получение токена из письма по Login при сбросе пароля"):
            if attempt == 0:
                raise AssertionError(f'Не удалось получить письмо с логином {login}')
            emails = self.get_api_v2_messages(limit=50).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]
                    print(token)
                    return token
            time.sleep(2)
            print('try')
            return self.get_token_by_login(login=login, attempt=attempt - 1)

    def delete_all_messages(self):
        with allure.step("Удаление всех писем"):
            response = self.client.delete(path='/api/v1/messages')
        return response

# if __name__ == '__main__':
# MailhogApi().get_api_v2_messages(limit=1)
