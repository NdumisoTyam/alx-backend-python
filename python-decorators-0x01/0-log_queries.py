import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from either kwargs or the first positional arg
        query = kwargs.get('query')
        if query is None and args:
            query = args[0]

        # Log the query
        print(f"Executing query: {query}")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # This will print: Executing query: SELECT * FROM users
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)