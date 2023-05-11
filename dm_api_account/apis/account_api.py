from requests import Response
from ..models.registration_model import RegistrationModel
from ..models.reset_password_model import ResetPasswordModel
from ..models.change_email_model import ChangeEmailModel
from ..models.change_password_model import ChangePasswordModel
from restclient.restclient import Restclient
from dm_api_account.models.user_envelope_model import UserEnvelopeModel
from dm_api_account.models.registration_model import RegistrationModel
from dm_api_account.models.user_details_envelope import UserDetailsEnvelopeModel
from dm_api_account.models.bad_request_error import BadRequestError
from dm_api_account.models.reset_password_model import ResetPasswordModel
from dm_api_account.models.change_password_model import ChangePasswordModel
from dm_api_account.models.change_email_model import ChangeEmailModel
from dm_api_account.models.general_error import GeneralError

class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_account(self, json: RegistrationModel, **kwargs) -> Response:
        """
        :param json registration_model
        Register new user
        :return:
        """
        response = self.client.post(
            path=f"/v1/account",
            json=json.dict(by_alias=True, exclude_none=True),
            **kwargs
        )
        RegistrationModel(**response.json())
        return response

    def post_v1_account_password(self, json: ResetPasswordModel, **kwargs) -> Response:
        """
        Reset registered user password
        :param json: reset_password_model
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/password",
            json=json.dict(by_alias=True, exclude_none=True),
            **kwargs
        )
        ResetPasswordModel(**response.json())

        UserEnvelopeModel(**response.json())
        """for 201 Created"""

        BadRequestError(**response.json())
        """for 400 Created"""

        return response

    def put_v1_account_email(self, json: ChangeEmailModel, **kwargs) -> RuntimeError:
        """
        Change registered user email
        :param json: change_email_model
        :return:
        """
        response = self.client.put(
            path=f"/v1/account/email",
            json=json.dict(by_alias=True, exclude_none=True),
            **kwargs
        )
        ChangeEmailModel(**response.json())
        UserEnvelopeModel(**response.json())
        BadRequestError(**response.json())
        return response

    def put_v1_account_password(self, json: ChangePasswordModel, **kwargs) -> Response:
        """
        Change registered user password
        :param :json change_password_model
        :return:
        """

        response = self.client.put(
            path=f"/v1/account/password",
            json=json.dict(by_alias=True, exclude_none=True),
            **kwargs
        )
        ChangePasswordModel(**response.json())
        UserEnvelopeModel(**response.json())
        BadRequestError(**response.json())

        return response

    def put_v1_account_token(self, token: str, **kwargs) -> Response:
        """
        Activate registered user
        :return:
        """

        response = self.client.put(
            path=f"/v1/account/{token}",
            **kwargs
        )
        UserEnvelopeModel(**response.json())
        GeneralError(**response.json())
        return response

    def get_v1_account(self, **kwargs):
        """
        Get current user
        :return:
        """

        response = self.client.get(
            path=f"/v1/account",
            **kwargs
        )
        UserDetailsEnvelopeModel(**response.json())
        return response
