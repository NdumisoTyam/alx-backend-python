#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """Generator that yields one age at a time from user_data."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',        # Change if needed
        password='',        # Change if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]  # row is a tuple like (age,)

    cursor.close()
    conn.close()


def calculate_average_age():
    """Calculates and prints the average age using the stream_user_ages generator."""
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ 1st and only loop
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

#!/usr/bin/python3
import average_age  # assuming your file is named average_age.py

average_age.calculate_average_age()
