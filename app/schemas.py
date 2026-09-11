from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    """
    Base properties shared by BookCreate and Book schemas.
    """
    title: str = Field(..., min_length=1, description="Title of the book")
    author: str = Field(..., min_length=1, description="Author of the book")
    isbn: str = Field(..., min_length=10, max_length=13, description="10 or 13-digit ISBN code")
    price: float = Field(..., ge=0.0, description="Price of the book, must be non-negative")
    quantity: int = Field(default=0, ge=0, description="Quantity of books in stock, must be non-negative")
    published_year: int = Field(..., ge=0, le=2100, description="Year the book was published")

class BookCreate(BookBase):
    """
    Schema for creating a new Book. Inherits all fields from BookBase.
    """
    pass

class BookUpdate(BaseModel):
    """
    Schema for updating an existing Book. All fields are optional.
    """
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    price: Optional[float] = Field(None, ge=0.0)
    quantity: Optional[int] = Field(None, ge=0)
    published_year: Optional[int] = Field(None, ge=0, le=2100)

class Book(BookBase):
    """
    Schema representing a Book returned from the API. Includes the auto-generated database ID.
    """
    id: int

    # Configures Pydantic to read data from SQLAlchemy ORM models (objects)
    model_config = ConfigDict(from_attributes=True)
