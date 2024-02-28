import os
import datetime
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

class User(db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserName = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(40), nullable=False)
    Role = db.Column(db.String(20), nullable=False)

user_parser = reqparse.RequestParser()
user_parser.add_argument('UserName', type=str, required=True, help='UserName is required')
user_parser.add_argument('Password', type=str, required=True, help='Password is required')
user_parser.add_argument('Role', type=str, required=True, help='Role is required')

class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_data = {
                    'UserId' : user.UserId,
                    'UserName' : user.UserName,
                    'Password' : user.Password,
                    'Role' : user.Role
                }
                return user_data, 200
            else:
                return "User not found", 404
        else:
            users = User.query.all()
            users_data = []
            for user in users:
                user_data = {
                    'UserId' : user.UserId,
                    'UserName' : user.UserName,
                    'Password' : user.Password,
                    'Role' : user.Role
                }
                users_data.append(user_data)
            return users_data, 200
        
    # def get(self, user_id):
    #     user = User.query.get(user_id)
    #     if user:
    #         user_data = {
    #             'UserId' : user.UserId,
    #             'UserName' : user.UserName,
    #             'Passwod' : user.Password,
    #             'Role' : user.Role
    #         }
    #         return user_data, 200
    #     else:
    #         return "User not found", 404
    
    def post(self):
        args = user_parser.parse_args()
        new_user = User(
            UserName=args['UserName'],
            Password=args['Password'],
            Role=args['Role']
        )
        db.session.add(new_user)
        db.session.commit()
        return "User added successfully", 201
    
    def put(self, user_id):
        args = user_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            user.UserName = args['UserName']    
            user.Password = args['Password']    
            user.Role = args['Role']
            db.session.commit()
            return f"User with {user_id} updated successfully" , 200
        else:
            return f"User with {user_id} not found", 404  

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f"User with ID {user_id} Deleted", 200
        else:
            return f"User with id {user_id} not found", 400

api.add_resource(UserAPI, "/API/Users")

class Section(db.Model):
    __tablename__ = 'section'
    SectionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Title = db.Column(db.String(50), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Description = db.Column(db.Text, nullable=False)
    ImageLink = db.Column(db.String(255))

section_parser = reqparse.RequestParser()
section_parser.add_argument('Title', type=str, required=True, help='Title is required')
section_parser.add_argument('Description', type=str, required=True, help='Description is required')
section_parser.add_argument('ImageLink', type=str)
class SectionAPI(Resource):
    def get(self, section_id):
        section = Section.query.get(section_id)
        if section:
            section_data = {
                'SectionId': section.SectionId,
                'Title': section.Title,
                'CreatedDate': section.CreatedDate.strftime('%Y-%m-%d %H:%M:%S'),
                'Description': section.Description,
                'ImageLink': section.ImageLink
            }
            return section_data, 200
        else:
            return "Section not found", 404
    
    def post(self):
        args = section_parser.parse_args()
        new_section = Section(
            Title=args['Title'],
            Description=args['Description'],
            ImageLink=args['ImageLink']
        )
        db.session.add(new_section)
        db.session.commit()
        return "Section added successfully", 201
    
    def put(self, section_id):
        args = section_parser.parse_args()
        section = Section.query.get(section_id)
        if section:
            section.Title = args['Title']
            section.Description = args['Description']
            section.ImageLink = args['ImageLink']
            db.session.commit()
            return f"Section with ID {section_id} updated successfully", 200
        else:
            return f"Section with ID {section_id} not found", 404
    
    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return f"Section with ID {section_id} deleted successfully", 200
        else:
            return f"Section with ID {section_id} not found", 404

api.add_resource(SectionAPI, "/API/Sections")

# book = Book.query.all()
print(Section.query.all())

## This is Sample I created to learn sql lite connectivity
# class Book(db.Model):
#     __tablename__ = 'book'
#     ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     Name = db.Column(db.String, unique=True, nullable=False)
#     Date_created = db.Column(db.String, nullable=False)
#     Description = db.Column(db.String)

# parser = reqparse.RequestParser()
# parser.add_argument('Name')
# parser.add_argument('Date_created')
# parser.add_argument('Description')

# class BookAPI(Resource):
#     def get(self):
#         book_obj = Book.query.all()
#         all_book = {}
#         i = 1
#         for book in book_obj:
#             this_book = {}
#             this_book['ID'] = book.ID
#             this_book['Name'] = book.Name
#             this_book['Date_created'] = book.Date_created
#             this_book['Description'] = book.Description
#             all_book[f'Book_{i}'] = this_book
#             i+=1
#         return all_book
    
#     def post(self):
#         args = parser.parse_args()
#         new_book = Book(Name = args['Name'], Date_created = args['Date_created'], Description = args['Description'])
#         db.session.add(new_book)
#         db.session.commit()
#         return "Added successfully", 201
    
#     def put(self, ID):
#         to_update = Book.query.get(ID)
#         args = parser.parse_args()
#         to_update.Name = args["Name"]
#         to_update.Date_created = args["Date_created"]
#         to_update.Description = args["Description"]
#         db.session.commit()
#         return f"Updated data for {ID} Successfully"

#     def delete(self, ID):
#         to_delete = Book.query.get(ID)
#         db.session.delete(to_delete)
#         db.session.commit()
#         return f"Deleted data for {ID} Successfully"

# api.add_resource(BookAPI, "/API/AllBooks", "/API/AddBooks", "/API/<int:ID>/UpdateBooks", "/API/<int:ID>/DeleteBooks")


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

# @app.route("/adminLogin", methods = ["GET","POST"])
# def admin():
#     book = Book.query.all()
#     return render_template("home.html", book=book)


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