from mariadb import connect
from mariadb.connections import Connection


def get_connection() -> Connection:
    return connect(
        user="root",
        password="123",
        host="localhost",
        port=3306,
        database="learning_platform"
    )


def read_query(sql: str, sql_params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        return list(cursor)


def insert_query(sql: str, sql_params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.lastrowid


def update_query(sql: str, sql_params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.rowcount


def delete_query(sql: str, sql_params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.rowcount
