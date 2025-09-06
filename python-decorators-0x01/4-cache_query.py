import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Determine the SQL query string from kwargs or positional args
        query = kwargs.get('query')
        if query is None and args:
            query = args[0]

        # Return cached result if available
        if query in query_cache:
            return query_cache[query]

        # Execute the query, cache the result, then return
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call – cache miss, executes the SQL
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call:", users)

    # Second call – cache hit, returns immediately
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call:", users_again)