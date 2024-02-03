from flask import redirect, render_template, session
from functools import wraps
import requests
import hidden


def apology(message, code=400):
    def filter(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)

        return s

    return render_template("apology.html", top=code, bottom=filter(message)), code


def input_validation(query):
    author = query["inauthor"]
    isbn = query["isbn"]
    title = query["intitle"]

    if author:
        if author.isnumeric():
            return (None, "Please enter valid author name")
        query["inauthor"] = author.lower()

    if isbn:
        if not isbn.isnumeric():
            return (None, "Isbn number should only contain digits")

    if title:
        query["intitle"] = title.lower()
        query["intitle"] = '"' + title + '"'

    return (query,)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_books(url):
    try:
        response = requests.get(url)
        response.raise_for_status

        bk_info = response.json()

        if bk_info["totalItems"] == 0:
            return None

        books = []
        name = hidden.get_names()

        for book in bk_info["items"]:
            bk = book["volumeInfo"]

            if all(bk.get(nm) for nm in name):
                bk["publishedDate"] = bk["publishedDate"][0:4]
                books.append(bk)

        return books

    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        return None


api_key = hidden.get_api_key()


def subject_lookup(sub):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{sub}&startIndex=0&maxResults=30&key={api_key}"

    return get_books(url)


def query_lookup(query):
    para = ""
    for qr in query:
        if not query[qr] == "":
            para += qr + ":" + query[qr] + "+"
    para = para[:-1]
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={para}&startIndex=0&maxResults=20&printType=books&key={api_key}"

    return get_books(url)


def bk_mark_lookup(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&startIndex=0&maxResults=20&printType=books&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status

        bk_info = response.json()

        if bk_info["totalItems"] == 0:
            return None

        books = bk_info["items"][0]
        bk = books["volumeInfo"]
        bk["publishedDate"] = bk["publishedDate"][:4]

        return bk

    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        return None


