import psycopg2

from table_queries import (
    user_submission_table,
    submitted_cases_table,
    users_tables,
)
from postgres_conn import PostgresConnection


def create():
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        table_queries = [
            user_submission_table,
            submitted_cases_table,
            users_tables,
        ]
        for table_query in table_queries:
            try:
                cursor.execute(table_query)
            except psycopg2.IntegrityError as e:
                pass
        print("Created tables")


if __name__ == "__main__":
    create()
