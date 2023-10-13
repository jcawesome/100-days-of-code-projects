from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# from flask_wtf import FlaskForm

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)


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
# with app.app_context():
#     db.create_all()

# Using a list to store books information - DEPRECATED
# all_books = []


# class LibraryForm(FlaskForm):
#     pass

@app.route('/')
def home():
    # READ ALL RECORDS
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD into DB
        with app.app_context():
            new_book = Books(title=request.form['title'],
                             author=request.form['author'],
                             rating=request.form['rating']
                             )
            db.session.add(new_book)
            db.session.commit()

        # Append to all_book list - DEPRECATED
        # new_book = {
        #     "title": request.form['title'],
        #     "author": request.form['author'],
        #     "rating": request.form['rating']
        # }
        # all_books.append(new_book)
        return redirect(url_for('home'))
    # form = LibraryForm()
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Books, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Books, book_id)
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Books, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
