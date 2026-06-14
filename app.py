import re

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")

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

        print(first_name)
        print(last_name)
        print(phone_number)
        print(email)
        print(role)

        return "Form received successfully"
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)