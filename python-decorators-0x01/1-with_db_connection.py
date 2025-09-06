import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a connection to the users.db SQLite database
        conn = sqlite3.connect('users.db')
        try:
            # Inject the connection as the first positional argument
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is always closed
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    # Fetch user with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)