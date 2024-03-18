import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from distutils.log import debug 
from fileinput import filename 

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

api.add_resource(UserAPI, "/API/Users", "/API/Users/<int:user_id>")


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
    def get(self, section_id=None):
        if section_id:
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
        else:
            sections = Section.query.all()
            sections_data = []
            for section in sections:
                section_data = {
                    'SectionId': section.SectionId,
                    'Title': section.Title,
                    'CreatedDate': section.CreatedDate.strftime('%Y-%m-%d %H:%M:%S'),
                    'Description': section.Description,
                    'ImageLink': section.ImageLink
                }
                sections_data.append(section_data)
            return sections_data, 200
    
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

api.add_resource(SectionAPI, "/API/Sections", "/API/Sections/<int:section_id>")

class Books(db.Model):
    __tablename__ = 'books'
    BookId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    SectionId = db.Column(db.Integer, db.ForeignKey('section.SectionId'), nullable=False)
    Title = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.Text)
    ImageLink = db.Column(db.String(255))


book_parser = reqparse.RequestParser()
book_parser.add_argument('SectionId', type=int, required=True,help="SectionID is required")
book_parser.add_argument('Title', type=str, required=True,help="Title is required")
book_parser.add_argument('Author', type=str, required=True,help="Author is required")
book_parser.add_argument('Content', type=str)
book_parser.add_argument('ImageLink', type=str)

class BooksAPI(Resource):
    def get(self, book_id=None):
        if book_id:
            book = Books.query.get(book_id)
            if book:
                book_data = {
                    "BookId" : book.BookId,
                    "SectionId" : book.SectionId,
                    "Title" : book.Title,
                    "Author" : book.Author,
                    "Content": book.Content,
                    "ImageLink":book.ImageLink
                }
                return book_data, 200
            else:
                return f"No Book with {book_id} found", 400
        else:
            books = Books.query.all()
            books_data = []
            for book in books:
                book_data = {
                    "BookId" : book.BookId,
                    "SectionId" : book.SectionId,
                    "Title" : book.Title,
                    "Author" : book.Author,
                    "Content": book.Content,
                    "ImageLink":book.ImageLink
                }
                books_data.append(book_data)
            return books_data, 200
        
    def post(self):
        args = book_parser.parse_args()
        new_section = Books(
            SectionId = args['SectionId'],
            Title = args['Title'],
            Author = args['Author'],
            Content = args['Content'],
            ImageLink = args['ImageLink']
        )
        db.session.add(new_section)
        db.session.commit()
        return "Book added successfully", 200

    def put(self, book_id):
        args = book_parser.parse_args()
        book = Books.query.get(book_id)
        if book:
            book.SectionId = args['SectionId']
            book.Title = args['Title']
            book.Author = args['Author']
            book.Content = args['Content']
            book.ImageLink = args['ImageLink']
            db.session.commit()
            return f"Book data updated for {book_id}", 200
        else:
            return f"Book for ID {book_id} not found", 400
    
    def delete(self, book_id):
        book = Books.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return f"Book for ID {book_id} deleted", 200
        else:
            return f"No book with {book_id} found", 400

api.add_resource(BooksAPI,"/API/Books", "/API/Books/<int:book_id>")


class BookIssue(db.Model):
    __tablename__ = 'BookIssue'
    IssueId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey(Books.BookId), nullable=False)
    SectionId = db.Column(db.Integer, db.ForeignKey(Section.SectionId), nullable=False)
    RequestDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Days = db.Column(db.Integer, nullable=False)
    IssueDate = db.Column(db.String)
    IssueStatus = db.Column(db.String, nullable=False)
    LastIssueStatusDate = db.Column(db.String)

BookIssue_parser = reqparse.RequestParser()
BookIssue_parser.add_argument('UserId', type=int, required=True, help='UserId is required')
BookIssue_parser.add_argument('BookId', type=int, required=True, help='BookId is required')
BookIssue_parser.add_argument('SectionId', type=int, required=True, help='SectionId is required')
BookIssue_parser.add_argument('Days', type=int, required=True, help='Days is required')
BookIssue_parser.add_argument('IssueDate', type=str)
BookIssue_parser.add_argument('IssueStatus', type=str, required=True, help='IssueStatus is required')
BookIssue_parser.add_argument('LastIssueStatusDate', type=str)


class BookIssueApi(Resource):
    def get(self, issue_id=None):
        if issue_id:
            issue = BookIssue.query.get(issue_id)
            if issue:
                issue_data = {
                    "IssueId" : issue.IssueId,
                    "UserId" : issue.UserId,
                    "BookId" : issue.BookId,
                    "SectionId" : issue.SectionId,
                    "RequestDate" : issue.RequestDate.strftime('%Y-%m-%d %H:%M:%S'),
                    "Days" : issue.Days,
                    "IssueDate" : issue.IssueDate,
                    "IssueStatus" : issue.IssueStatus,
                    "LastIssueStatusDate" : issue.LastIssueStatusDate,
                }
                return issue_data, 200
            else:
                return f"No issue with {issue_id}"
        else:
            issues = BookIssue.query.all()
            issues_data = []
            for issue in issues:
                issue_data = {
                "IssueId" : issue.IssueId,
                "UserId" : issue.UserId,
                "BookId" : issue.BookId,
                "SectionId" : issue.SectionId,
                "RequestDate" : issue.RequestDate.strftime('%Y-%m-%d %H:%M:%S'),
                "Days" : issue.Days,
                "IssueDate" : issue.IssueDate,
                "IssueStatus" : issue.IssueStatus,
                "LastIssueStatusDate" : issue.LastIssueStatusDate,
                }
                issues_data.append(issue_data)
            return issues_data, 200
    
    def post(self):
        args = BookIssue_parser.parse_args()
        new_issue = BookIssue(
            UserId = args["UserId"],
            BookId = args["BookId"],
            SectionId = args["SectionId"],
            Days = args["Days"],
            IssueDate = args["IssueDate"],
            IssueStatus = args["IssueStatus"],
            LastIssueStatusDate = args["LastIssueStatusDate"]
        )
        db.session.add(new_issue)
        db.session.commit()
        return "Book added successfully", 200
    
    def put(self, issue_id):
        args = BookIssue_parser.parse_args()
        issue = BookIssue.query.get(issue_id)
        if issue:
            issue.UserId = args["UserId"]
            issue.BookId = args["BookId"]
            issue.SectionId = args["SectionId"]
            issue.Days = args["Days"]
            issue.IssueDate = args["IssueDate"]
            issue.IssueStatus = args["IssueStatus"]
            issue.LastIssueStatusDate = args["LastIssueStatusDate"]
            db.session.commit()
            return f"Book Issue Updated for {issue_id}"
        else:
            return f"No Issue found with {issue_id}"
    
    def delete(self, issue_id):
        issue = BookIssue.query.get(issue_id)
        if issue:
            db.session.delete(issue)
            db.session.commit()
            return f"Issue deleted with ID {issue_id}",200
        else:
            return f"No issue found with {issue_id}",400

api.add_resource(BookIssueApi,"/API/BookIssue","/API/BookIssue/<int:issue_id>")


@app.route("/", methods = ["GET","POST"])
def home():
    return render_template("start.html")

@app.route("/user-login", methods = ["GET","POST"])
def userLogin():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data['username'])
        try:
            user = User.query.filter_by(UserName=data['username']).first()
            print("UserName",user.UserName)
            print("Password",user.Password)
            print("UserId",user.UserId)
            userid = user.UserId

            if user:
                if user.Password == data["password"]:
                    return redirect(url_for('allBooks', userid = userid))
                else:
                    return render_template("user-login.html", error="Wrong Password")
            else:
                return render_template("user-login.html", error="No user with this Username")
        except:
            return render_template("user-login.html", error="No user with this Username")
    else:
        return render_template("user-login.html")

@app.route("/register", methods = ["GET","POST"])
def userRegister():
    if request.method =='POST':
        data = request.form.to_dict()
        user = User.query.filter_by(UserName=data['Username']).first()
        if user:
            return render_template("user-login.html", error="User already registered please login!")
        else:
            user = User(UserName=data['Username'], Password=data['password'], Role='user')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('userLogin'))
    else:
        return render_template("user-register.html")

@app.route("/librarian-login", methods = ["GET","POST"])
def librarianLogin():
    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)
        try:
            user = User.query.filter_by(UserName=data['username']).first()
            if user:
                if user.Password == data["password"]:
                    return redirect(url_for('addSection'))
                    # return render_template("add-section.html")
                else:
                    return render_template("librarian-login.html", error="Wrong Password")
            else:
                return render_template("librarian-login.html", error="No user with this Username")
        except:
            return render_template("librarian-login.html", error="No user with this Username")
    else:
        return render_template("librarian-login.html")

@app.route("/add-section", methods = ["GET","POST"])
def addSection():
    if request.method == 'POST':
        data = request.form.to_dict()
        section = Section(Title=data['section'], Description=data['text'])
        db.session.add(section)
        db.session.commit()
        print(data)
        section = Section.query.all()
        return render_template("add-section.html", section = section)
    else:
        section = Section.query.all()
        return render_template("add-section.html", section = section)

@app.route("/showBooks", methods = ["GET","POST"])
def showBooks():
    if request.method == 'POST': 
        f = request.files['file']
        file_path = os.path.join("books", f.filename)
        f.save(file_path) 
        data = request.form.to_dict()
        print(data)
        books = Books(SectionId = data['book_section'],Title=data['Book-Title'],Author=data['Author'],Content=data['Content'])
        db.session.add(books)
        db.session.commit()
        print(data)
        books = Books.query.all()
        return render_template("showBooks.html", books=books)
    else:
        books = Books.query.all()
        return render_template("showBooks.html", books=books)

@app.route("/deleteBook/<int:bookId>", methods=["GET", "POST"])
def deleteBook(bookId):
    book = Books.query.get(bookId)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('showBooks'))

@app.route("/deleteSecion/<int:sectionId>", methods=["GET", "POST"])
def deleteSection(sectionId):
    section = Section.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()
    return redirect(url_for('addSection'))

@app.route("/updateBooks/<int:BooksId>", methods=["GET", "POST"])
def updateBooks(BooksId):
    book = Books.query.get(BooksId)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        data = request.form.to_dict()
        book.SectionId = 1
        book.Title = data['Title']
        book.Author = data['Author']
        book.Content = data['Content']

        db.session.commit()

        return redirect(url_for('showBooks'))
    else:
        books = Books.query.all()
        return render_template("showBooks.html", books=books)

#    IssueId
#     UserId
#     BookId
#     SectionId
#     RequestDate
#     Days
#     IssueDate = db.Column(db.String)
#     IssueStatus = db.Column(db.String, nullable=False)
#     LastIssueStatusDate = db.Column(db.String)


@app.route("/allBooks", methods=["GET","POST"])
def allBooks():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        requstBook = BookIssue(UserId=data['userid'], BookId=data['bookid'], SectionId=data['sectionId'], Days=data['days'], IssueStatus = 'requested', IssueDate = datetime.datetime.today().date())
        db.session.add(requstBook)
        db.session.commit()

        books = Books.query.all()
        userid = data['userid']
        return render_template("allBooks.html", books=books, userid = userid)
    else:
        books = Books.query.all()
        userid = request.args.get('userid')
        return render_template("allBooks.html", books=books, userid = userid)

@app.route("/myBooks", methods=["GET","POST"])
def myBooks():
    books = Books.query.all()
    return render_template("myBooks.html", books= books)

if __name__ == '__main__':
    app.run(debug=True)
