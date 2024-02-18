# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
