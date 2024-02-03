from flask import Flask, request, render_template, redirect, session, flash
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import string
import hidden
from helpers import (
    apology,
    login_required,
    query_lookup,
    subject_lookup,
    input_validation,
    bk_mark_lookup,
)


db = SQL("sqlite:///biblioteca.db")


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    with open("image_url.txt", "r") as file:
        categories = []

        for subs in file:
            subs, img = subs.split(":", maxsplit=1)
            subs = string.capwords(subs)
            categories.append(
                {
                    "sub": subs.replace("&", "").replace("  ", " "),
                    "img": img.replace("&w=400", "&w=600"),
                }
            )

    session["categories"] = categories

    return render_template("index.html")


@app.route("/search")
@login_required
def search():
    query = {
        "intitle": request.args.get("title"),
        "inauthor": request.args.get("author"),
        "isbn": request.args.get("isbn"),
    }

    if all(query[qr] == "" for qr in query):
        return apology("Please enter at least one search term", 400)

    user_input = input_validation(query)

    if not user_input[0]:
        return apology(user_input[1], 400)

    session["bookinfo"] = query_lookup(query)

    return render_template("results.html")


@app.route("/search/subjects")
@login_required
def search_subject():
    subject = request.args.get("subject")

    if not subject:
        return apology("Not a Valid Request", 400)
    subject = '"' + subject + '"'
    session["bookinfo"] = subject_lookup(subject)

    return render_template("results.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("username and password both required", 400)

        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not len(user) == 1 or not check_password_hash(user[0]["hash"], password):
            return apology("Invalid username and/or passsword", 400)

        session["user_id"] = user[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password:
            return apology("username and password both required", 400)

        if not confirmation:
            return apology("both password fields needs to get filled up", 400)

        if not password == confirmation:
            return apology("both password needs to get matched", 400)

        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already taken", 400)

        session["user_id"] = db.execute(
            "INSERT INTO users (username, hash) VALUES (?,?)",
            username,
            generate_password_hash(password),
        )

        return redirect("/")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/addbookmark")
@login_required
def add_bookmark():
    if request.args.get("isbn"):
        isbn = request.args.get("isbn")

    db.execute(
        "INSERT INTO bookmarks (id, isbn) VALUES (?, ?)", session["user_id"], isbn
    )

    return ("", 204)


@app.route("/rvbookmark")
@login_required
def rv_bookmark():
    if request.args.get("isbn"):
        isbn = request.args.get("isbn")

    db.execute(
        "DELETE FROM bookmarks WHERE id = ? AND isbn = ?", session["user_id"], isbn
    )

    return ("", 204)


@app.route("/mybooks")
@login_required
def my_books():
    books = db.execute("SELECT isbn FROM bookmarks WHERE id = ?", session["user_id"])

    bookmarks = []

    if books:
        for bk in books:
            bk_info = bk_mark_lookup(bk["isbn"])
            print(bk_info)

            if bk_info:
                bookmarks.append(bk_info)

    session["bookmarks"] = bookmarks

    return render_template("mybooks.html")


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


@app.route("/settings/username", methods=["POST"])
@login_required
def setting_username():
    jsonData = request.get_json()

    username = jsonData.get("name")
    password = jsonData.get("pass")

    if not username or not password:
        return ("every field is required", 433)

    user = db.execute("SELECT * FROM users WHERE id is ?", session["user_id"])

    if not check_password_hash(user[0]["hash"], password):
        return ("Password didn't matched", 434)

    if username == user[0]["username"]:
        return ("That's your existing username", 435)

    if db.execute("SELECT * FROM users WHERE username = ?", username):
        return ("username already taken", 436)

    db.execute(
        "UPDATE users SET username = ? WHERE id = ?", username, session["user_id"]
    )

    return ("", 204)


@app.route("/settings/password", methods=["POST"])
@login_required
def setting_password():
    jsonData = request.get_json()

    current_pass = jsonData.get("cpassword")
    new_pass = jsonData.get("npassword")
    confirm_pass = jsonData.get("confirmpassword")

    if not current_pass or not new_pass or not confirm_pass:
        return ("every field is required", 433)

    if check_password_hash(
        db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0][
            "hash"
        ],
        current_pass,
    ):
        if new_pass == confirm_pass:
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?",
                generate_password_hash(confirm_pass),
                session["user_id"],
            )
            return ("", 204)

        else:
            return ("Passwords needs to get matched", 435)

    else:
        return ("Current Password didn't matched", 434)
