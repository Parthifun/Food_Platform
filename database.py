
def create_restaurant(
    owner_email,
    restaurant_name,
    phone_number,
    address,
    cuisine_type
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO restaurants
        (
            owner_email,
            restaurant_name,
            phone_number,
            address,
            cuisine_type
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        owner_email,
        restaurant_name,
        phone_number,
        address,
        cuisine_type
    ))

    conn.commit()
    conn.close()

def get_restaurants_by_owner(owner_email):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM restaurants
        WHERE owner_email = ?
        """,
        (owner_email,)
    )

    restaurants = cursor.fetchall()

    conn.close()

    return restaurants

def get_restaurant_by_id(restaurant_id):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM restaurants
        WHERE id = ?
        """,
        (restaurant_id,)
    )

    restaurant = cursor.fetchone()

    conn.close()

    return restaurant

def get_menu_items_by_restaurant(restaurant_id):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM menu_items
        WHERE restaurant_id = ?
        """,
        (restaurant_id,)
    )

    menu_items = cursor.fetchall()

    conn.close()

    return menu_items


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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        owner_email TEXT NOT NULL,

        restaurant_name TEXT NOT NULL,

        phone_number TEXT NOT NULL,

        address TEXT NOT NULL,

        cuisine_type TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        restaurant_id INTEGER NOT NULL,

        item_name TEXT NOT NULL,

        description TEXT,

        price REAL NOT NULL,

        category TEXT NOT NULL

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        restaurant_id INTEGER NOT NULL,

        item_name TEXT NOT NULL,

        description TEXT,

        price REAL NOT NULL,

        category TEXT NOT NULL

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