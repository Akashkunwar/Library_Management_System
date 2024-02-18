import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"library.db")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

api = Api(app)
class Book(db.Model):
    __tablename__ = 'book'
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String, unique=True, nullable=False)
    Date_created = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserName = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Role = db.Column(db.String)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

# book = Book.query.all()
print(User.query.all())