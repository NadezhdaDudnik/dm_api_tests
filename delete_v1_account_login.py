import requests


def delete_v1_account_login():
    """
    Logout as current user
    :return:
    """
    url = "http://localhost:5051/v1/account/login"

    headers = {
        'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3uEeVpwTryYujIU6qaU2sIYfhtd8UdpN9VZD7pXr/m+GRlWZd5Gqh3v2iGI5HpKph8=',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="DELETE",
        url=url,
        headers=headers
    )
    return response


response = delete_v1_account_login()
