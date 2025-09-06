import sqlite3
import functools

def with_db_connection(func):
    """
    Opens an SQLite connection, passes it into the wrapped function,
    then always closes the connection afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Wraps a DB operation in a transaction.
    Commits on success, rolls back on any exception.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )

if __name__ == "__main__":
    # This call will automatically:
    # 1. Open the DB connection
    # 2. Start a transaction
    # 3. Execute the UPDATE
    # 4. Commit (or rollback on error)
    # 5. Close the connection
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')