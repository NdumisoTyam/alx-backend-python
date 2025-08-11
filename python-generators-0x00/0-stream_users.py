#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that streams rows from user_data table one at a time as dicts."""
    # Connect to the ALX_prodev database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',       # change if needed
        password='',       # change if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")

    # Single loop to fetch rows one by one and yield them
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row

    cursor.close()
    conn.close()
