import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from data_models import db, Author, Book

# ------------------------------------------------------------
# 1. Ensure that the 'data/' directory exists
# ------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ------------------------------------------------------------
# 2. Configure the Flask app and initialize SQLAlchemy
# ------------------------------------------------------------
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(DATA_DIR, 'library.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secret key is required for flashing messages
app.secret_key = "ein_sehr_geheimes_schluesselchen_123"

db.init_app(app)


# ------------------------------------------------------------
# 3. Routes
# ------------------------------------------------------------
@app.route("/")
def home():
    """
    Display the home page:
    - Allow sorting by title or author
    - Allow keyword search on book titles
    - Render the template with books matching criteria
    """
    # Sorting parameter from URL (default: "title")
    sort_by = request.args.get("sort", "title")
    # Search parameter from URL (e.g., ?search=Kafka)
    search_term = request.args.get("search", "").strip()

    # Base query: load books along with their author in one go
    query = Book.query.options(joinedload(Book.author))

    # If a search term is provided, filter by title using a case-insensitive LIKE
    if search_term:
        query = query.filter(Book.title.ilike(f"%{search_term}%"))

    # Apply sorting: by author name or by book title
    if sort_by == "author":
        query = query.join(Author).order_by(Author.name, Book.title)
    else:
        query = query.order_by(Book.title)

    books = query.all()
    no_results = bool(search_term and not books)

    return render_template(
        "home.html",
        books=books,
        current_sort=sort_by,
        search_term=search_term,
        no_results=no_results,
    )


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Handle adding a new author:
    - GET: render the add_author.html form
    - POST: validate input, create Author, flash success or error
    """
    if request.method == "POST":
        name = request.form.get("name").strip()
        birth_date = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death") or None

        # Validate that name and birth date are provided
        if not name or not birth_date:
            flash("Name und Geburtsdatum sind erforderlich.", "error")
            return redirect(url_for("add_author"))

        new_author = Author(
            name=name, birth_date=birth_date, date_of_death=date_of_death
        )
        db.session.add(new_author)
        db.session.commit()

        flash(f"Autor:in «{new_author.name}» wurde erfolgreich hinzugefügt.", "success")
        return redirect(url_for("add_author"))

    # Render form on GET request
    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Handle adding a new book:
    - GET: render the add_book.html form along with existing authors
    - POST: validate input, ensure unique ISBN, create Book, flash success or error
    """
    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        title = request.form.get("title").strip()
        isbn = request.form.get("isbn").strip()
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")

        # Validate that all fields are provided
        if not title or not isbn or not publication_year or not author_id:
            flash(
                "Alle Felder sind erforderlich (Titel, ISBN, Jahr, Autor).", "error"
            )
            return redirect(url_for("add_book"))

        # Check for existing book with same ISBN
        exists = Book.query.filter_by(isbn=isbn).first()
        if exists:
            flash(f"Ein Buch mit ISBN «{isbn}» existiert bereits.", "error")
            return redirect(url_for("add_book"))

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=int(publication_year),
            author_id=int(author_id),
        )
        db.session.add(new_book)
        db.session.commit()

        flash(f"Buch «{new_book.title}» wurde erfolgreich hinzugefügt.", "success")
        return redirect(url_for("add_book"))

    # Render form on GET request
    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Delete a book (and its author if orphaned):
    - Remove the Book by ID
    - If the author has no more books, delete the author as well
    - Flash a confirmation message and redirect to home
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    # Delete the book first
    db.session.delete(book)
    db.session.commit()

    # Check if the author has any remaining books
    remaining_books = Book.query.filter_by(author_id=author.id).count()
    if remaining_books == 0:
        # Delete author if no books remain
        db.session.delete(author)
        db.session.commit()
        flash(
            f"Buch «{book.title}» und Autor:in «{author.name}» wurden gelöscht.",
            "success",
        )
    else:
        flash(f"Buch «{book.title}» wurde gelöscht.", "success")

    return redirect(url_for("home"))


# ------------------------------------------------------------
# 4. Create tables once and start the app
# ------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
