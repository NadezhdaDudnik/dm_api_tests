from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_delete_v1_account_login():
    api = Facade(host='http://localhost:5051')
    response = api.login_api.delete_v1_account_login()
    print(response)
