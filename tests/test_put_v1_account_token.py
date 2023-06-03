# from services.dm_api_account import Facade
# from generic.helpers.mailhog import MailhogApi
# import structlog
# from hamcrest import assert_that, has_properties
# from dm_api_account.models.user_envelope_model import UserRole

# structlog.configure(
#    processors=[
#        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
#    ]
# )
from generic.helpers.orm_models import User


def test_put_v1_account_token(dm_api_facade, dm_orm):
    login = "login24"
    dm_orm.update_user_activated(login=login)
    dataset = dm_orm.get_user_by_login(login=login)
    row: User
    for row in dataset:
        assert row.Activated is True, f'User {login} is not activated'

    # dm_api_facade.account.activate_registered_user(login=login)

# mailhog = MailhogApi(host='http://localhost:5025')
# api = Facade(host='http://localhost:5051')
# token = mailhog.get_token_from_last_email()
# response = api.account_api.put_v1_account_token(token=token)
# assert_that(response.resource, has_properties(
#    {
#       "login": "login20",
#      "roles": [UserRole.guest, UserRole.player]
# }
# ))
