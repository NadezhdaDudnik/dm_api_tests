from services.dm_api_account import DmApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_delete_v1_account_login_all():
    api = DmApiAccount(host='http://localhost:5051')
    response = api.login.delete_v1_account_login_all()
    assert response.status_code == 200, f'Status code of response should be equal 200 but equals {response.status_code}'
    print(response)

