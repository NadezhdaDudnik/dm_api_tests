def test_post_v1_account_password(dm_api_facade):
    login = "login40"
    email = "login40@mail.ru"
    dm_api_facade.account.reset_password(
        login=login,
        email=email
    )
    response = dm_api_facade.account.confirm_link_after_reset_password(login=login)
    return response
