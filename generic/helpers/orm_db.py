from typing import List

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from generic.helpers.orm_models import User

from orm_client.orm_client import OrmClient


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select([User])
        dataset = self.db.send_query(query)
        return dataset

    def get_user_by_login(self, login) -> List[User]:
        query = select([User]).where(User.Login == login)
        dataset = self.db.send_query(query)
        return dataset

    def delete_user_by_login(self, login):
        query = delete(User).where(User.Login == login)
        dataset = self.db.send_bulk_query(query)
        return dataset

    def update_user_activated(self, login, is_activated: bool = True):
        query = update(User).where(User.Login == login).values({User.Activated: is_activated})
        dataset = self.db.send_bulk_query(query)
        return dataset
