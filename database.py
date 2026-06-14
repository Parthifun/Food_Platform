import sqlite3

def create_database():
    conn = sqlite3.connect("food_platform.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,

        phone_number TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully")

def get_user_by_email(email):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_user_by_phone(phone_number):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE phone_number = ?",
        (phone_number,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def create_user(
    first_name,
    last_name,
    phone_number,
    email,
    password,
    role
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (
            first_name,
            last_name,
            phone_number,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        first_name,
        last_name,
        phone_number,
        email,
        password,
        role
    ))

    conn.commit()
    conn.close()

def get_user_by_login(login_identifier):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        OR phone_number = ?
    """,
    (
        login_identifier,
        login_identifier
    ))

    user = cursor.fetchone()

    conn.close()

    return user

create_database()    