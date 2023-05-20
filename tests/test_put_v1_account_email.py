from dm_api_account.models.change_email_model import ChangeEmail
from services.dm_api_account import Facade
import structlog
from generic.helpers.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = Facade(host='http://localhost:5051')
    json = ChangeEmail(
         login="login16",
         password="login_55",
         email="login166@mail.ru"
    )
    response = api.account_api.put_v1_account_email(json=json)
    token = mailhog.get_token_from_last_email()
    api.account_api.put_v1_account_token(token=token)
    print(response)
