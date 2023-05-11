from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import RegistrationModel

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host='http://localhost:5051')
    json = RegistrationModel(
        login="login19",
        email="login19@mail.ru",
        password="login_55"
    )
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'Status code of response should be equal 201 but equals {response.status_code}'
    token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=token)

