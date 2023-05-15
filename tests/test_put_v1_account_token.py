import json
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from hamcrest import assert_that, has_properties
from dm_api_account.models.user_envelope_model import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host='http://localhost:5051')
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
        {
            "login": "login20",
            "roles": [UserRole.guest, UserRole.player]
        }
    ))



