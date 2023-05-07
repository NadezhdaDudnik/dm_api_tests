from services.dm_api_account import DmApiAccount


def test_put_v1_account_email():
    api = DmApiAccount(host='http://localhost:5051')
    json = {
        "login": "login10",
        "password": "login_555",
        "email": "login100@mail.ru"
    }
    response = api.account.put_v1_account_email(
        json=json
    )
    print(response)

