import requests


def put_v1_account_email():
    """
    Change registered user email
    :return:
    """
    url = "http://localhost:5051/v1/account/email"

    payload = {
        "login": "login10",
        "password": "login_555",
        "email": "login100@mail.ru"
    }
    headers = {
        'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3uEeVpwTryYujIU6qaU2sIYfhtd8UdpN9VZD7pXr/m+GRlWZd5Gqh3v2iGI5HpKph8=',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="PUT",
        url=url,
        headers=headers,
        json=payload
    )
    return response


response = put_v1_account_email()