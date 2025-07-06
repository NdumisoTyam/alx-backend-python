#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data table in batches of size batch_size."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',      # change if needed
        password='',      # change if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")

    def stream_users_in_batches(batch_size):
    ...
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # ✅ Correct


    cursor.close()
    conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # ✅ Correct: use yield


