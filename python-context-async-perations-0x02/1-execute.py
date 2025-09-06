import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_path='users.db'):
        self.query = query
        self.params = params or ()
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # open the database connection
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # execute the query with parameters
        self.cursor.execute(self.query, self.params)

        # fetch all results
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        # close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # use the context manager to execute and retrieve results
    with ExecuteQuery(query, params) as users_over_25:
        for user in users_over_25:
            print(user)