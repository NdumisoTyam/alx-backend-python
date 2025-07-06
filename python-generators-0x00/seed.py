import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',      # Change if needed
            password=''       # Change if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    """Connects specifically to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',    # Change if needed
            password='',    # Change if needed
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX idx_user_id (user_id)
        );
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    """Inserts data from CSV into the user_data table, avoiding duplicates."""
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use UUID from CSV or generate if missing
            user_id = row.get('user_id') or str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']

            # Check if user_id already exists
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                continue  # Skip duplicate

            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, age)
            )
    connection.commit()
    cursor.close()

def stream_user_data(connection):
    """Generator that yields one row at a time from user_data."""
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
