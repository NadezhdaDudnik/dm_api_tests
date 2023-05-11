from dm_api_account.models.login_credentials_model import LoginCredentialsModel
from services.dm_api_account import DmApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    api = DmApiAccount(host='http://localhost:5051')
    json = LoginCredentialsModel(
         login="login16",
         password="login_55",
         rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json)
    assert response.status_code == 200, f'Status code of response should be equal 200 but equals {response.status_code}'
    print(response)
