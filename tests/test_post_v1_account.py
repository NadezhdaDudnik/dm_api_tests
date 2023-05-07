from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host='http://localhost:5051')
    json = {
        "login": "login10",
        "email": "login10@mail.ru",
        "password": "login_55"
    }
    response = api.account.post_v1_account(
        json=json
    )
    print(response)
