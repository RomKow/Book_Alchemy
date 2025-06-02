"""
seed_data.py

Populate the database with initial authors and books.
Run this script once to add five authors and twenty books.
"""

from app import app
from data_models import db, Author, Book
import datetime

with app.app_context():
    # ---------------------------
    # 1. Create 5 authors
    # ---------------------------
    author1 = Author(
        name="Jane Austen",
        birth_date=datetime.date(1775, 12, 16),
        date_of_death=datetime.date(1817, 7, 18),
    )
    author2 = Author(
        name="George Orwell",
        birth_date=datetime.date(1903, 6, 25),
        date_of_death=datetime.date(1950, 1, 21),
    )
    author3 = Author(
        name="J.K. Rowling",
        birth_date=datetime.date(1965, 7, 31),
        date_of_death=None,
    )
    author4 = Author(
        name="Gabriel García Márquez",
        birth_date=datetime.date(1927, 3, 6),
        date_of_death=datetime.date(2014, 4, 17),
    )
    author5 = Author(
        name="Fyodor Dostoevsky",
        birth_date=datetime.date(1821, 11, 11),
        date_of_death=datetime.date(1881, 2, 9),
    )

    db.session.add_all([author1, author2, author3, author4, author5])
    db.session.commit()

    # ---------------------------
    # 2. Create 20 books
    # ---------------------------
    # Jane Austen (author1.id)
    book1 = Book(
        title="Pride and Prejudice",
        isbn="9780141199078",
        publication_year=1813,
        author_id=author1.id,
    )
    book2 = Book(
        title="Sense and Sensibility",
        isbn="9780141439662",
        publication_year=1811,
        author_id=author1.id,
    )
    book3 = Book(
        title="Emma",
        isbn="9780141439587",
        publication_year=1815,
        author_id=author1.id,
    )
    book4 = Book(
        title="Mansfield Park",
        isbn="9780141439792",
        publication_year=1814,
        author_id=author1.id,
    )

    # George Orwell (author2.id)
    book5 = Book(
        title="1984",
        isbn="9780451524935",
        publication_year=1949,
        author_id=author2.id,
    )
    book6 = Book(
        title="Animal Farm",
        isbn="9780451526342",
        publication_year=1945,
        author_id=author2.id,
    )
    book7 = Book(
        title="Homage to Catalonia",
        isbn="9780156421171",
        publication_year=1938,
        author_id=author2.id,
    )
    book8 = Book(
        title="Down and Out in Paris and London",
        isbn="9780141182631",
        publication_year=1933,
        author_id=author2.id,
    )

    # J.K. Rowling (author3.id)
    book9 = Book(
        title="Harry Potter and the Sorcerer's Stone",
        isbn="9780439554930",
        publication_year=1997,
        author_id=author3.id,
    )
    book10 = Book(
        title="Harry Potter and the Chamber of Secrets",
        isbn="9780439064866",
        publication_year=1998,
        author_id=author3.id,
    )
    book11 = Book(
        title="Harry Potter and the Prisoner of Azkaban",
        isbn="9780439136365",
        publication_year=1999,
        author_id=author3.id,
    )
    book12 = Book(
        title="Harry Potter and the Goblet of Fire",
        isbn="9780439139595",
        publication_year=2000,
        author_id=author3.id,
    )

    # Gabriel García Márquez (author4.id)
    book13 = Book(
        title="One Hundred Years of Solitude",
        isbn="9780060883287",
        publication_year=1967,
        author_id=author4.id,
    )
    book14 = Book(
        title="Love in the Time of Cholera",
        isbn="9780307389732",
        publication_year=1985,
        author_id=author4.id,
    )
    book15 = Book(
        title="Chronicle of a Death Foretold",
        isbn="9780060954032",
        publication_year=1981,
        author_id=author4.id,
    )
    book16 = Book(
        title="The Autumn of the Patriarch",
        isbn="9780060914272",
        publication_year=1975,
        author_id=author4.id,
    )

    # Fyodor Dostoevsky (author5.id)
    book17 = Book(
        title="Crime and Punishment",
        isbn="9780140449136",
        publication_year=1866,
        author_id=author5.id,
    )
    book18 = Book(
        title="The Brothers Karamazov",
        isbn="9780140449242",
        publication_year=1880,
        author_id=author5.id,
    )
    book19 = Book(
        title="Notes from Underground",
        isbn="9780140449181",
        publication_year=1864,
        author_id=author5.id,
    )
    book20 = Book(
        title="Demons",
        isbn="9780140449266",
        publication_year=1872,
        author_id=author5.id,
    )

    db.session.add_all(
        [
            book1,
            book2,
            book3,
            book4,
            book5,
            book6,
            book7,
            book8,
            book9,
            book10,
            book11,
            book12,
            book13,
            book14,
            book15,
            book16,
            book17,
            book18,
            book19,
            book20,
        ]
    )
    db.session.commit()

    print("Seeder: 5 authors and 20 books have been added successfully.")
