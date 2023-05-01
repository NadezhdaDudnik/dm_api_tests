import requests


def get_v1_account():
    """
    Get current user
    :return:
    """
    url = "http://localhost:5051/v1/account"

    headers = {
        'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3tSjxTsDEJrXRPW+7nr8wvYMZWFwROnyXUUh9zf1jn5DDYIzEuNIAUR7PxWJnirYYs=',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="GET",
        url=url,
        headers=headers
    )
    return response

