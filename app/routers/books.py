from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book record. Checks for ISBN duplicates.
    """
    db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists."
        )
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of books with optional pagination (skip & limit).
    """
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific book by its ID. Returns 404 if not found.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """
    Update a book's details. Checks if the new ISBN clashes with an existing book.
    Returns 404 if the book does not exist.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # If the user tries to update the ISBN, verify that it doesn't conflict with another book
    if book_update.isbn is not None and book_update.isbn != db_book.isbn:
        isbn_conflict = crud.get_book_by_isbn(db, isbn=book_update.isbn)
        if isbn_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another book with this ISBN already exists."
            )
            
    return crud.update_book(db=db, db_book=db_book, book_update=book_update)

@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database. Returns 404 if the book does not exist.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return crud.delete_book(db=db, db_book=db_book)
