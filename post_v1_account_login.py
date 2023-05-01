import requests


def post_v1_account_login():
    """
    Authenticate via credentials
    :return:
    """
    url = "http://localhost:5051/v1/account/login"

    payload = {
        "login": "login10",
        "password": "login_55",
        "rememberMe": True
    }
    headers = {
        'X-Dm-Bb-Render-Mode': '<string>',
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload
    )
    return response


response = post_v1_account_login()