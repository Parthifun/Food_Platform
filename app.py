import re

from flask import Flask, render_template, request, session, redirect, url_for
from database import (
    create_restaurant,
    get_menu_items_by_restaurant,
    get_restaurant_by_id,
    get_restaurants_by_owner,
    get_user_by_email,
    get_user_by_login,
    get_user_by_phone,
    create_user,
    create_menu_item,
    get_menu_item_by_id,
    update_menu_item,
    delete_menu_item,
    update_restaurant,
    get_all_restaurants,
    get_orders_by_restaurant,
    add_to_cart,
    get_cart_items,
    remove_cart_item,
    increase_quantity,
    decrease_quantity,
    create_order,
    get_orders_by_customer,
    create_database,
    update_order_status,
    load_sample_data,
    clear_cart,
    create_order_item
)
app = Flask(__name__)
app.secret_key = "food_platform_secret_key"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dev_login")
def dev_login():

    return render_template(
        "dev_login.html"
    )

@app.route("/dev_customer")
def dev_customer():

    session["first_name"] = "Customer"
    session["email"] = "customer@test.com"
    session["role"] = "Customer"

    return redirect(url_for("dashboard"))

@app.route("/dev_owner")
def dev_owner():

    session["first_name"] = "Restaurant Owner"
    session["email"] = "owner@test.com"
    session["role"] = "Restaurant Owner"

    return redirect(url_for("dashboard"))

@app.route("/dev_admin")
def dev_admin():

    session["first_name"] = "Admin"
    session["email"] = "admin@test.com"
    session["role"] = "Admin"

    return redirect(url_for("dashboard"))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        login_identifier = request.form["login_identifier"]
        password = request.form["password"]

        user = get_user_by_login(login_identifier)

        if not user:
            return "User not found."

        if user[5] != password:
            return "Invalid password."

        session["first_name"] = user[1]
        session["email"] = user[4]
        session["role"] = user[6]
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "first_name" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        first_name=session["first_name"],
        role=session["role"]
    )

@app.route("/add_restaurant", methods=["GET", "POST"])
def add_restaurant():

    if "first_name" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    if request.method == "POST":

        restaurant_name = request.form["restaurant_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        cuisine_type = request.form["cuisine_type"]

        create_restaurant(
            session["email"],
            restaurant_name,
            phone_number,
            address,
            cuisine_type
        )

        return render_template("success_restaurant.html")

    return render_template("add_restaurant.html")

@app.route("/view_restaurants")
def view_restaurants():

    if "email" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    restaurants = get_restaurants_by_owner(
        session["email"]
    )

    return render_template(
        "view_restaurants.html",
        restaurants=restaurants
    )

@app.route("/restaurants")
def customer_restaurants():

    restaurants = get_all_restaurants()

    return render_template(
        "customer_restaurants.html",
        restaurants=restaurants
    )

@app.route("/customer_restaurant/<int:restaurant_id>")
def customer_restaurant_details(restaurant_id):

    restaurant = get_restaurant_by_id(
        restaurant_id
    )

    menu_items = get_menu_items_by_restaurant(
        restaurant_id
    )

    return render_template(
        "customer_restaurant_details.html",
        restaurant=restaurant,
        menu_items=menu_items
    )

@app.route("/restaurant/<int:restaurant_id>")
def restaurant_details(restaurant_id):

    if "email" not in session:
        return redirect(url_for("login"))
    
    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    restaurant = get_restaurant_by_id(
        restaurant_id
    )

    menu_items = get_menu_items_by_restaurant(
        restaurant_id
    )

    return render_template(
        "restaurant_details.html",
        restaurant=restaurant,
        menu_items=menu_items
    )



@app.route(
    "/restaurant/<int:restaurant_id>/add_menu_item",
    methods=["GET", "POST"]
)
def add_menu_item(restaurant_id):

    if "email" not in session:
        return redirect(url_for("login"))
    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    if request.method == "POST":

        item_name = request.form["item_name"]
        description = request.form["description"]
        price = request.form["price"]
        category = request.form["category"]

        create_menu_item(
            restaurant_id,
            item_name,
            description,
            price,
            category
        )

        return redirect(
            url_for(
                "restaurant_details",
                restaurant_id=restaurant_id
            )
        )

    return render_template(
        "add_menu_item.html"
    )

@app.route(
    "/edit_menu_item/<int:menu_item_id>",
    methods=["GET", "POST"]
)
def edit_menu_item(menu_item_id):

    if "email" not in session:
        return redirect(url_for("login"))
    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    menu_item = get_menu_item_by_id(menu_item_id)

    if request.method == "POST":

        item_name = request.form["item_name"]
        description = request.form["description"]
        price = request.form["price"]
        category = request.form["category"]

        update_menu_item(
            menu_item_id,
            item_name,
            description,
            price,
            category
        )

        return redirect(
            url_for(
                "restaurant_details",
                restaurant_id=menu_item[1]
            )
        )

    return render_template(
        "edit_menu_item.html",
        menu_item=menu_item
    )

@app.route("/delete_menu_item/<int:menu_item_id>")
def delete_menu_item_route(menu_item_id):

    if "email" not in session:
        return redirect(url_for("login"))

    menu_item = get_menu_item_by_id(menu_item_id)

    restaurant_id = menu_item[1]

    delete_menu_item(menu_item_id)

    return redirect(
        url_for(
            "restaurant_details",
            restaurant_id=restaurant_id
        )
    )

@app.route("/add_to_cart/<int:menu_item_id>")
def add_to_cart_route(menu_item_id):

    if "email" not in session:
        return redirect(url_for("login"))

    menu_item = get_menu_item_by_id(menu_item_id)

    restaurant_id = menu_item[1]

    success = add_to_cart(
        session["email"],
        restaurant_id,
        menu_item_id
    )

    if not success:
        return render_template(
            "cart_restaurant_conflict.html"
        )

    return redirect(
        url_for(
            "customer_restaurant_details",
            restaurant_id=restaurant_id
        )
    )

@app.route("/cart")
def cart():

    if "email" not in session:
        return redirect(url_for("login"))

    cart_items = get_cart_items(
        session["email"]
    )

    total = 0

    for item in cart_items:
        total += item[4]

    print("CART ITEMS =", cart_items)
    print("TOTAL =", total)

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )

@app.route("/increase_quantity/<int:cart_id>")
def increase_quantity_route(cart_id):

    increase_quantity(cart_id)

    return redirect(url_for("cart"))


@app.route("/decrease_quantity/<int:cart_id>")
def decrease_quantity_route(cart_id):

    decrease_quantity(cart_id)

    return redirect(url_for("cart"))

@app.route("/remove_cart_item/<int:cart_id>")
def remove_cart_item_route(cart_id):

    if "email" not in session:
        return redirect(url_for("login"))

    remove_cart_item(cart_id)

    return redirect(url_for("cart"))

@app.route("/profile")
def profile():

    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("profile.html")

@app.route("/checkout")
def checkout():

    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("checkout.html")


@app.route("/payment", methods=["POST"])
def payment():

    if "email" not in session:
        return redirect(url_for("login"))

    order_type = request.form["order_type"]

    return render_template(
        "payment.html",
        order_type=order_type
    )

@app.route("/order_success", methods=["POST"])
def order_success():

    if "email" not in session:
        return redirect(url_for("login"))

    payment_method = request.form["payment_method"]
    order_type = request.form["order_type"]

    cart_items = get_cart_items(
        session["email"]
    )
    print("ORDER SUCCESS CART =", cart_items)
    if not cart_items:
        return "Cart is empty."
    restaurant_id = cart_items[0][5]

    total = 0

    for item in cart_items:
        total += item[4]

    order_id = create_order(
        session["email"],
        restaurant_id,
        total,
        order_type,
        payment_method
    )
    for item in cart_items:

        create_order_item(
            order_id,
            item[6],
            item[3]
        )

    clear_cart(
    session["email"]
    )

    return render_template(
        "order_success.html"
    )

@app.route("/orders")
def orders():

    if "email" not in session:
        return redirect(url_for("login"))

    orders = get_orders_by_customer(
        session["email"]
    )

    return render_template(
        "orders.html",
        orders=orders
    )

@app.route("/order/<int:order_id>")
def order_details(order_id):

    if "email" not in session:
        return redirect(url_for("login"))

    orders = get_orders_by_customer(
        session["email"]
    )

    order = None

    for current_order in orders:

        if current_order[0] == order_id:
            order = current_order
            break

    if not order:
        return "Order not found."

    return render_template(
        "order_details.html",
        order=order
    )

@app.route(
    "/update_order_status/<int:order_id>/<status>"
)
def update_order_status_route(
    order_id,
    status
):

    if "email" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    update_order_status(
        order_id,
        status
    )

    return redirect(
        url_for("owner_orders")
    )

@app.route("/owner_orders")
def owner_orders():

    if "email" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Restaurant Owner":
        return "Access Denied"

    restaurants = get_restaurants_by_owner(
        session["email"]
    )

    all_orders = []

    for restaurant in restaurants:

        restaurant_orders = get_orders_by_restaurant(
            restaurant[0]
        )

        all_orders.extend(
            restaurant_orders
        )

    return render_template(
        "owner_orders.html",
        orders=all_orders
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

@app.route("/register" , methods=["GET", "POST"])
def register():
    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]
        if password != confirm_password:
            return "Password and Confirm Password do not match."

        if get_user_by_email(email):
            return "Email already exists."

        if get_user_by_phone(phone_number):
            return "Phone number already exists."

        create_user(
            first_name,
            last_name,
            phone_number,
            email,
            password,
            role
        )

        return "Registration Successful"
    return render_template("register.html")

if __name__ == "__main__":

    create_database()
    load_sample_data()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )