from ..models.login_credentials_model import LoginCredentialsModel
from requests import session, Response
from restclient.restclient import Restclient
from dm_api_account.models.user_envelope_model import UserEnvelopeModel
from dm_api_account.models.login_credentials_model import LoginCredentialsModel
from dm_api_account.models.bad_request_error import BadRequestError
from dm_api_account.models.general_error import GeneralError


class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_account_login(self, json: LoginCredentialsModel, **kwargs) -> Response:
        """
        Authenticate via credentials
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/login",
            json=json.dict(by_alias=True, exclude_none=True),
            **kwargs
        )
        LoginCredentialsModel(**response.json())
        UserEnvelopeModel(**response.json())
        BadRequestError(**response.json())
        GeneralError(**response.json())

        return response

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login",
            **kwargs
        )
        GeneralError(**response.json())

        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login/all",
            **kwargs
        )

        GeneralError(**response.json())
        return response
