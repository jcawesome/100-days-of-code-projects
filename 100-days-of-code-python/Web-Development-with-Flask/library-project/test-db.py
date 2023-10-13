import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()
# cursor.execute("CREATE TABLE books "
#                "(id INTEGER PRIMARY KEY, "
#                "title varchar(250) NOT NULL UNIQUE, "
#                "author varchar(250) NOT NULL,"
#                "rating FLOAT NOT NULL)")

cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()

# USING SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# Create table schema in the database. Requires application context.
# initial creation of table in DB
with app.app_context():
    db.create_all()

# CREATE RECORD
with app.app_context():
    new_book = Books(title="Harry Potter 2", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()

# READ ALL RECORDS
with app.app_context():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()

# UPDATE RECORD
with app.app_context():
    book_to_update = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
    book_to_update.title = "Harry Potter and the Philosopher's Stone"
    db.session.commit()

# DELETE A Particular Record By PRIMARY KEY
book_id = 2
with app.app_context():
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
