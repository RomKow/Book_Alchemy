from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object for use in models
db = SQLAlchemy()


class Author(db.Model):
    """
    Author model represents a book author.

    Attributes:
        id (int): Auto-incrementing primary key.
        name (str): Full name of the author.
        birth_date (date): Author's birth date.
        date_of_death (date or None): Author's death date, optional.
        books (Relationship): List of Book instances linked via foreign key.
    """
    __tablename__ = "authors"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    birth_date = db.Column(
        db.Date,
        nullable=False
    )
    date_of_death = db.Column(
        db.Date,
        nullable=True
    )

    # Define one-to-many relationship: an author can have multiple books
    books = db.relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        """
        Return an unambiguous string representation of the Author.
        """
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Return a readable string representation of the Author.
        """
        return f"Author {self.name} (ID {self.id})"


class Book(db.Model):
    """
    Book model represents a book in the library.

    Attributes:
        id (int): Auto-incrementing primary key.
        isbn (str): Unique ISBN identifier.
        title (str): Title of the book.
        publication_year (int): Year the book was published.
        author_id (int): Foreign key pointing to the Author.
        author (Relationship): The Author instance linked to this book.
    """
    __tablename__ = "books"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    isbn = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )
    title = db.Column(
        db.String(200),
        nullable=False
    )
    publication_year = db.Column(
        db.Integer,
        nullable=False
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False
    )

    # Define many-to-one relationship: each book has exactly one author
    author = db.relationship(
        "Author",
        back_populates="books"
    )

    def __repr__(self):
        """
        Return an unambiguous string representation of the Book.
        """
        return (
            f"<Book(id={self.id}, title='{self.title}', "
            f"isbn='{self.isbn}', year={self.publication_year})>"
        )

    def __str__(self):
        """
        Return a readable string representation of the Book.
        """
        return f"Book '{self.title}' ({self.publication_year})"
