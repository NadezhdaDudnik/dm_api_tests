import requests


def post_v1_account_password():
    """
    Reset registered user password
    :return:
    """
    url = "http://localhost:5051/v1/account/password"

    payload = {
        "login": "login10",
        "email": "login10@mail.ru"
    }
    headers = {
        'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3tSjxTsDEJrXRPW+7nr8wvYMZWFwROnyXUUh9zf1jn5DDYIzEuNIAUR7PxWJnirYYs=',
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


response = post_v1_account_password()