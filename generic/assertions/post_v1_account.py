import time

from hamcrest import assert_that, has_entries
from generic.helpers.orm_db import OrmDatabase


class AssertionsPostV1Account:
    def __init__(self, orm_db: OrmDatabase):
        self.orm_db = orm_db

    def check_user_was_created(self, login):
        dataset = self.orm_db.get_user_by_login(login=login)
        row: User
        for row in dataset:
            assert_that(row, has_entries(
                {
                    'Login': login,
                    'Activated': False
                }
            ))
            # assert row.Login == login, f'User {login} is not registered'
        # assert row.Activated is False, f'User {login} is was activated'

    def check_user_update_activation(self, login):
        self.orm_db.update_user_activated(login=login)
        dataset = self.orm_db.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True, f'User {login} is not activated'

    def check_user_was_activated(self, login):
        dataset = self.orm_db.get_user_by_login(login=login)
        time.sleep(2)
        for row in dataset:
            assert row.Activated is True, f'User {login} is not activated'
