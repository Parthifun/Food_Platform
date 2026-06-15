
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

from itertools import count
import sqlite3

def create_menu_item(
    restaurant_id,
    item_name,
    description,
    price,
    category
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO menu_items
        (
            restaurant_id,
            item_name,
            description,
            price,
            category
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        restaurant_id,
        item_name,
        description,
        price,
        category
    ))

    conn.commit()
    conn.close()

def get_menu_item_by_id(menu_item_id):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM menu_items
        WHERE id = ?
        """,
        (menu_item_id,)
    )

    menu_item = cursor.fetchone()

    conn.close()

    return menu_item

def update_menu_item(
    menu_item_id,
    item_name,
    description,
    price,
    category
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE menu_items
        SET
            item_name = ?,
            description = ?,
            price = ?,
            category = ?
        WHERE id = ?
        """,
        (
            item_name,
            description,
            price,
            category,
            menu_item_id
        )
    )

    conn.commit()
    conn.close()

def delete_menu_item(menu_item_id):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM menu_items
        WHERE id = ?
        """,
        (menu_item_id,)
    )

    conn.commit()
    conn.close()

def update_restaurant(
    restaurant_id,
    restaurant_name,
    phone_number,
    address,
    cuisine_type
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE restaurants
        SET
            restaurant_name = ?,
            phone_number = ?,
            address = ?,
            cuisine_type = ?
        WHERE id = ?
        """,
        (
            restaurant_name,
            phone_number,
            address,
            cuisine_type,
            restaurant_id
        )
    )

    conn.commit()
    conn.close()

def get_all_restaurants():

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM restaurants
        ORDER BY restaurant_name
    """)

    restaurants = cursor.fetchall()

    conn.close()

    return restaurants

def add_menu_items(cursor, restaurant_id, items):

    for item_name, description, price, category in items:

        cursor.execute("""
            INSERT INTO menu_items
            (
                restaurant_id,
                item_name,
                description,
                price,
                category
            )
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            restaurant_id,
            item_name,
            description,
            price,
            category
        ))

def load_sample_data():

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM restaurants")
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return

    restaurants = [

    (
        "Hyd House",
        "9891111111",
        "123 Main St, Saginaw, MI",
        "Hyderabadi",
        [
            ("Chicken Dum Biryani", "Authentic Hyderabadi biryani", 15.99, "Biryani"),
            ("Mutton Dum Biryani", "Slow cooked mutton biryani", 18.99, "Biryani"),
            ("Chicken 65", "Spicy chicken starter", 11.99, "Starter"),
            ("Apollo Fish", "Hyderabad special fish fry", 13.99, "Starter"),
            ("Irani Chai", "Traditional tea", 2.99, "Drinks")
        ]
    ),

    (
        "Lakshmi Mess",
        "9892222222",
        "456 State St, Saginaw, MI",
        "South Indian",
        [
            ("Idli", "Steamed rice cakes", 5.99, "Breakfast"),
            ("Vada", "Lentil donut", 4.99, "Breakfast"),
            ("Masala Dosa", "Potato stuffed dosa", 9.99, "Breakfast"),
            ("Veg Meals", "Traditional meals", 12.99, "Meals"),
            ("Filter Coffee", "South Indian coffee", 3.49, "Drinks")
        ]
    ),

    (
        "Punjabi Dhaba",
        "9893333333",
        "789 Center Rd, Saginaw, MI",
        "Punjabi",
        [
            ("Butter Chicken", "Creamy chicken curry", 14.99, "Main Course"),
            ("Paneer Butter Masala", "Paneer curry", 12.99, "Main Course"),
            ("Dal Makhani", "Black lentils", 10.99, "Main Course"),
            ("Garlic Naan", "Fresh naan", 3.99, "Bread"),
            ("Sweet Lassi", "Traditional lassi", 4.49, "Drinks")
        ]
    ),

    (
        "Dragon Chinese Kitchen",
        "9894444444",
        "321 Bay Rd, Saginaw, MI",
        "Chinese",
        [
            ("Chicken Fried Rice", "Wok tossed rice", 11.99, "Rice"),
            ("Hakka Noodles", "Chinese noodles", 11.99, "Noodles"),
            ("Chicken Manchurian", "Spicy chicken", 13.99, "Main Course"),
            ("Spring Rolls", "Vegetable rolls", 5.99, "Starter"),
            ("Green Tea", "Hot tea", 2.99, "Drinks")
        ]
    ),

    (
        "Seoul Korean BBQ",
        "9895555555",
        "654 Gratiot Ave, Saginaw, MI",
        "Korean",
        [
            ("Bulgogi", "Marinated beef", 16.99, "Main Course"),
            ("Bibimbap", "Rice bowl", 14.99, "Main Course"),
            ("Kimchi Fried Rice", "Spicy rice", 12.99, "Rice"),
            ("Korean Fried Chicken", "Crispy chicken", 13.99, "Starter"),
            ("Korean Pear Juice", "Fresh juice", 4.99, "Drinks")
        ]
    ),

    (
        "Pizza Palace",
        "9896666666",
        "987 Main St, Saginaw, MI",
        "Italian",
        [
            ("Margherita Pizza", "Classic cheese pizza", 12.99, "Pizza"),
            ("Pepperoni Pizza", "Pepperoni pizza", 15.99, "Pizza"),
            ("Garlic Bread", "Toasted garlic bread", 5.99, "Sides"),
            ("Pasta Alfredo", "Creamy pasta", 11.99, "Pasta"),
            ("Tiramisu", "Italian dessert", 6.99, "Dessert")
        ]
    )
    ]

    for restaurant_name, phone, address, cuisine, items in restaurants:

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
            "owner@test.com",
            restaurant_name,
            phone,
            address,
            cuisine
        ))

        restaurant_id = cursor.lastrowid

        for item_name, description, price, category in items:

            cursor.execute("""
            INSERT INTO menu_items
            (
                restaurant_id,
                item_name,
                description,
                price,
                category
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                restaurant_id,
                item_name,
                description,
                price,
                category
            ))

    conn.commit()
    conn.close()

    print("Sample data loaded")

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
    CREATE TABLE IF NOT EXISTS cart (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_email TEXT NOT NULL,

        restaurant_id INTEGER NOT NULL,

        menu_item_id INTEGER NOT NULL,

        quantity INTEGER NOT NULL
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

def add_to_cart(
    customer_email,
    restaurant_id,
    menu_item_id
):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cart
        (
            customer_email,
            restaurant_id,
            menu_item_id,
            quantity
        )
        VALUES (?, ?, ?, 1)
    """,
    (
        customer_email,
        restaurant_id,
        menu_item_id
    ))

    conn.commit()
    conn.close()

def get_cart_items(customer_email):

    conn = sqlite3.connect("food_platform.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            cart.id,
            menu_items.item_name,
            menu_items.price,
            cart.quantity
        FROM cart
        JOIN menu_items
        ON cart.menu_item_id = menu_items.id
        WHERE cart.customer_email = ?
    """,
    (customer_email,)
    )

    cart_items = cursor.fetchall()

    conn.close()

    return cart_items

if __name__ == "__main__":
    create_database()
    load_sample_data()