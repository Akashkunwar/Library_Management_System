import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"library.db")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Book(db.Model):
    __tablename__ = 'book'
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String, unique=True, nullable=False)
    Date_created = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)

book = Book.query.all()
print(book)

@app.route("/", methods = ["GET","POST"])
def home():
    book = Book.query.all()
    return render_template("home.html", book=book)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

