from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host='http://localhost:5051')
    token = mailhog.get_token_from_last_email()
    json = {
        "login": "login17",
        "token": token,
        "oldPassword": "login_55",
        "newPassword": "login_555"
    }
    response = api.account.put_v1_account_password(json=json)
    assert response.status_code == 200, f'Status code of response should be equal 200 but equals {response.status_code}'
    print(response)



