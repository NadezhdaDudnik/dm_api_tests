from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    api = Facade(host='http://localhost:5051')
    login = "login28"
    email = "login28@mail.ru"
    password = "login_55"
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    api.account.activate_registered_user(login=login)
    api.login.login_user(login=login, password=password)
    token = api.login.get_auth_token(login='login27', password='login_55')
    api.account.set_headers(headers=token)
    api.login.set_headers(headers=token)
    api.login_api.delete_v1_account_login()
    #api.account.get_current_user_info()
    #api.login.logout_user_from_all_devices()
