import requests


def post_v1_account():
    """
    Register new user
    :return:
    """
    url = "http://localhost:5051/v1/account"

    payload = {
        "login": "login10",
        "email": "login10@mail.ru",
        "password": "login_55"
    }
    headers = {
        'X-Dm-Auth-Token': '<string>',
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


response = post_v1_account()
print(response.status_code)
print(response.request)
print(response.content)
print(response.url)
print(response.cookies)
print(response.json()['type'])
print(response.json()['title'])


print(response.request.url)
print(response.request.method)
print(response.request.headers)
print(response.request.body)