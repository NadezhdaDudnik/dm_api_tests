from typing import List

import allure
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from generic.helpers.orm_models import User

from orm_client.orm_client import OrmClient


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        with allure.step("Получение всех пользователей через БД"):
            query = select([User])
            dataset = self.db.send_query(query)
        return dataset

    with allure.step("Получение пользователя по login"):
        def get_user_by_login(self, login) -> List[User]:
            query = select([User]).where(User.Login == login)
            dataset = self.db.send_query(query)
            return dataset

    def delete_user_by_login(self, login):
        with allure.step("Удаление пользователя по Login через БД"):
            query = delete(User).where(User.Login == login)
            dataset = self.db.send_bulk_query(query)
        return dataset

    def update_user_activated(self, login, is_activated: bool = True):
        query = update(User).where(User.Login == login).values({User.Activated: is_activated})
        with allure.step("Активация пользователя через БД"):
            dataset = self.db.send_bulk_query(query)
        return dataset
