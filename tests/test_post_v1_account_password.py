from dm_api_account.models.reset_password_model import ResetPasswordModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host='http://localhost:5051')
    json = ResetPasswordModel(
         login="login16",
         email="login16@mail.ru"
    )
    response = api.account.post_v1_account_password(json=json)
    assert response.status_code == 200, f'Status code of response should be equal 200 but equals {response.status_code}'
    token = mailhog.get_token_from_last_email_reset()
    response = api.account.put_v1_account_token(token=token)
    print(response)
