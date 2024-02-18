# views.py

from flask import render_template
from models import Book

def start():
    return render_template("start.html")

def userLogin():
    return render_template("user-login.html")

def librarianLogin():
    return render_template("librarian-login.html")

def home():
    book = Book.query.all()
    return render_template("home.html", book=book)