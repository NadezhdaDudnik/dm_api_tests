import allure

from common_libs.db_client.db_client import DbClient

class DmDatabase:
    def __init__(self, user, password, host, database):
        self.db = DbClient(user, password, host, database)

    def get_all_users(self):
        with allure.step("Получение всех пользователей через БД"):
            query = 'select * from "public"."Users"'
            dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login):
        with allure.step("Получение пользователя по login"):
            query = f'''
            select * from "public"."Users"
            where "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login):
        with allure.step("Удаление пользователя по Login через БД"):
            query = f'''
            delete from "public"."Users" where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def update_user_activated(self, login, is_activated):
        with allure.step("Активация пользователя через БД"):
            query = f'''
            update "public"."Users" set "Activated" = '{is_activated}' where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
        return dataset
