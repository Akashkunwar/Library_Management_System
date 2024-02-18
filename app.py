# app.py

import os
from flask import Flask
from api import api
from models import db
from views import start, userLogin, librarianLogin

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"library.db")
db.init_app(app)
app.app_context().push()

app.add_url_rule("/", "start", start, methods=["GET", "POST"])
app.add_url_rule("/user-login", "userLogin", userLogin, methods=["GET", "POST"])
app.add_url_rule("/librarian-login", "librarianLogin", librarianLogin, methods=["GET", "POST"])

api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)


# # GET /API/AllBooks
# # POST/API/AddBooks
# # PUT /API/<int:ID>/UpdateBooks
# # DELETE /API/<int:ID>/DeleteBooks