import pymysql
import typing

from pymysql.cursors import DictCursor
from sqlalchemy.sql import ClauseElement
from contextlib import closing
from settings import DATABASE_CREDENTIALS


class Database:

    @staticmethod
    def conn():
        connection = pymysql.connect(
            host=DATABASE_CREDENTIALS['host'],
            user=DATABASE_CREDENTIALS['user'],
            password=DATABASE_CREDENTIALS['pass'],
            db=DATABASE_CREDENTIALS['database'],
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )

        return connection

    @staticmethod
    def execute_query(query: typing.Union[ClauseElement, str], res=False):
        with closing(Database.conn()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if res:
                    return cursor.fetchall()
