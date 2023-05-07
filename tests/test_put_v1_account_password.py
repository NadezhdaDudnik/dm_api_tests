from services.dm_api_account import DmApiAccount


def test_put_v1_account_password():
    api = DmApiAccount(host='http://localhost:5051')
    json = {
        "login": "login10",
        "token": "{token}",
        "oldPassword": "login_55",
        "newPassword": "login_555"
    }
    response = api.account.put_v1_account_password(
        json=json
    )
    print(response)



