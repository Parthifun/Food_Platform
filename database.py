import sqlite3

def create_database():
    conn = sqlite3.connect("food_platform.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,

        phone TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully")

create_database()    