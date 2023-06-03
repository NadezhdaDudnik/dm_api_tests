
def test_delete_v1_account_login_all(dm_api_facade):
    login = "login41"
    token = dm_api_facade.mailhog.get_token_by_login(login=login)
    dm_api_facade.login.set_headers(headers=token)
    dm_api_facade.login.logout_user_from_all_devices()

