import requests


def put_v1_account_token():
    """
    Activate registered user
    :return:
    """
    token = 'c4efef0c-6646-47c4-9ae9-3d74ca439dd6'
    url = f"http://localhost:5051/v1/account/{token}"

    headers = {
        'X-Dm-Auth-Token': '<string>',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="PUT",
        url=url,
        headers=headers
    )
    return response


response = put_v1_account_token()