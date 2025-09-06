import sqlite3

class DatabaseConnection:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        # Open and return the database connection
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # Always close the connection on exit
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # Use the context manager to query the users table
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)