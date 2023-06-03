
def test_put_v1_account_email(dm_api_facade):
    login = "login16"
    password = "login_55"
    email = "login166@mail.ru"
    dm_api_facade.account.change_email(
        login=login,
        password=password,
        email=email
    )
    response = dm_api_facade.account.activate_registered_user(login=login)
    return response

