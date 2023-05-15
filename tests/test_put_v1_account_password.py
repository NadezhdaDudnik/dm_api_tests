from dm_api_account.models.change_password_model import ChangePassword
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
    json = ChangePassword(
         login="login17",
         token=token,
         oldPassword="login_55",
         newPassword="login_555"
    )
    response = api.account.put_v1_account_password(json=json)
    print(response)



