from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class Book(Base):
    """
    SQLAlchemy model representing a Book in the bookstore inventory.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    published_year = Column(Integer, nullable=False)
