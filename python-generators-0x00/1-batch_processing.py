import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',       # Change as needed
        password='',       # Change as needed
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # ✅ uses yield

    cursor.close()
    conn.close()
    # ❌ no return here

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # ✅ uses yield only
    # ❌ no return here either

