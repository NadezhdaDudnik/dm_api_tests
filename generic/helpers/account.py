from apis.dm_api_account.models import Registration
from apis.dm_api_account.models import ResetPassword
from apis.dm_api_account.models import ChangeEmail
from apis.dm_api_account.models import ChangePassword
try:
    from services.dm_api_account import Facade
except ImportError:
    ...

class Account:
    def __init__(self, facade: Facade):
        self.facade = facade

    def set_headers(self, headers):
        self.facade.account_api.client.session.headers.update(headers)

    def register_new_user(self, login: str, email: str, password: str, status_code: int):
        response = self.facade.account_api.post_v1_account(
            json=Registration(
                login=login,
                email=email,
                password=password
            ),
            status_code=status_code
        )
        return response

    def activate_registered_user(self, login: str):
        token = self.facade.mailhog.get_token_by_login(login=login)
        response = self.facade.account_api.put_v1_account_token(token=token)
        return response

    def confirm_link_after_reset_password(self, login: str):
        token = self.facade.mailhog.get_token_from_last_email_reset(login=login)
        response = self.facade.account_api.put_v1_account_token(token=token)
        return response

    def get_current_user_info(self, **kwargs):
        response = self.facade.account_api.get_v1_account(**kwargs)
        return response

    def reset_password(self, login: str, email: str):
        response = self.facade.account_api.post_v1_account_password(
            json=ResetPassword(
                login=login,
                email=email
            )
        )
        return response

    def change_email(self, login: str, password: str, email: str):
        response = self.facade.account_api.put_v1_account_email(
            json=ChangeEmail(
                login=login,
                password=password,
                email=email
            )
        )
        return response

    def change_password(self, login: str, oldPassword: str, newPassword: str):
        response = self.facade.account_api.put_v1_account_email(
            json=ChangePassword(
                login=login,
                token=self.facade.mailhog.get_token_by_login(login=login),
                oldPassword=oldPassword,
                newPassword=newPassword
            )
        )
        return response
