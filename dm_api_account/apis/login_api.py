from ..models import *
from requests import Response
from restclient.restclient import Restclient
from ..utilities import validate_request_json, validate_status_code


class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_account_login(
            self,
            json: LoginCredentials,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope | BadRequestError | GeneralError:
        """
        Authenticate via credentials
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/login",
            json=validate_request_json(json)
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            UserEnvelope(**response.json())
        return response
    ''' elif response.status_code == 400:
         BadRequestError(**response.json())
     elif response.status_code == 403:
         GeneralError(**response.json())
     return response'''

    def delete_v1_account_login(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response | GeneralError:
        """
        Logout as current user
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login",
            **kwargs
        )

        validate_status_code(response, status_code)
        if response.status_code == 401:
            return GeneralError(**response.json())
        return response

    def delete_v1_account_login_all(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response | GeneralError:
        """
        Logout from every device
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login/all",
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 401:
            return GeneralError(**response.json())
        return response
