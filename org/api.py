# api.py

from flask_restful import Resource, Api, reqparse
from models import db, Book

api = Api()

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
        new_book = Book(Name=args['Name'], Date_created=args['Date_created'], Description=args['Description'])
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

