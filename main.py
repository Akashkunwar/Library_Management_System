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
# print(User.query.all())

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
    
    def put(self, ID):
        to_update = Book.query.get(ID)
        args = parser.parse_args()
        to_update.Name = args["Name"]
        to_update.Date_created = args["Date_created"]
        to_update.Description = args["Description"]
        db.session.commit()
        return f"Updated data for {ID} Successfully"

    def delete(self, ID):
        to_delete = Book.query.get(ID)
        db.session.delete(to_delete)
        db.session.commit()
        return f"Deleted data for {ID} Successfully"

api.add_resource(BookAPI, "/API/AllBooks", "/API/AddBooks", "/API/<int:ID>/UpdateBooks", "/API/<int:ID>/DeleteBooks")

@app.route("/", methods = ["GET","POST"])
def home():
    return render_template("start.html")

@app.route("/user-login", methods = ["GET","POST"])
def userLogin():
    return render_template("user-login.html")

@app.route("/librarian-login", methods = ["GET","POST"])
def librarianLogin():
    return render_template("librarian-login.html")

@app.route("/add-section", methods = ["GET","POST"])
def addSection():
    return render_template("add-section.html")

@app.route("/showBooks", methods = ["GET","POST"])
def showBooks():
    return render_template("showBooks.html")

@app.route("/adminLogin", methods = ["GET","POST"])
def admin():
    book = Book.query.all()
    return render_template("home.html", book=book)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )




# GET /API/AllBooks
# POST/API/AddBooks
# PUT /API/<int:ID>/UpdateBooks
# DELETE /API/<int:ID>/DeleteBooks