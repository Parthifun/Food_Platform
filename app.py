import re

from flask import Flask, render_template, request, session, redirect, url_for
from database import (
    get_user_by_email,
    get_user_by_login,
    get_user_by_phone,
    create_user
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