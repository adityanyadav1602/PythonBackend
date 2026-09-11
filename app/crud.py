from sqlalchemy.orm import Session
from app import models, schemas

def get_book(db: Session, book_id: int):
    """
    Retrieve a single book by its primary key ID.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_isbn(db: Session, isbn: str):
    """
    Retrieve a single book by its unique ISBN.
    Useful for checking duplicate entries.
    """
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of books with pagination.
    """
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    """
    Create a new book record in the database.
    """
    db_book = models.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        price=book.price,
        quantity=book.quantity,
        published_year=book.published_year
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: models.Book, book_update: schemas.BookUpdate):
    """
    Update an existing book record. 
    Only fields that are explicitly provided in the request (exclude_unset=True) will be modified.
    """
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: models.Book):
    """
    Delete a book record from the database.
    """
    db.delete(db_book)
    db.commit()
    return db_book
