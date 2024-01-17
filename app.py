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

# book = Book.query.all()

parser = reqparse.RequestParser()
parser.add_argument('Name')
parser.add_argument('Date_created')
parser.add_argument('Description')
class BookAPI(Resource):
    def get(self):
        book_obj = Book.query.all()
        all_book = {}
        i = 1
        for book in book_obj:
            this_book = {}
            this_book['ID'] = book.ID
            this_book['Name'] = book.Name
            this_book['Date_created'] = book.Date_created
            this_book['Description'] = book.Description
            all_book[f'Book_{i}'] = this_book
            i+=1
        return all_book
    
    def post(self):
        args = parser.parse_args()
        new_book = Book(Name = args['Name'], Date_created = args['Date_created'], Description = args['Description'])
        db.session.add(new_book)
        db.session.commit()
        return "Added successfully", 201

api.add_resource(BookAPI, "/API/AllBooks", "/API/AddBooks")

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
