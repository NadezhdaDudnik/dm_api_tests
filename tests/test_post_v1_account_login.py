from dm_api_account.models.login_credentials_model import LoginCredentials
from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    api = Facade(host='http://localhost:5051')
    login = "login29"
    password = "login_55"
    remember_me = True
    api.login.login_user(
         login=login,
         password=password,
         remember_me=remember_me
    )

