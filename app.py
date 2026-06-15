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
    update_menu_item
)
app = Flask(__name__)
app.secret_key = "food_platform_secret_key"

@app.route("/")
def home():
    return render_template("home.html")


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

    restaurants = get_restaurants_by_owner(
        session["email"]
    )

    return render_template(
        "view_restaurants.html",
        restaurants=restaurants
    )

@app.route("/restaurant/<int:restaurant_id>")
def restaurant_details(restaurant_id):

    if "email" not in session:
        return redirect(url_for("login"))

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

        return render_template("registration_success.html")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)