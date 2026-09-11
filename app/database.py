from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL. This will create a file named "books.db" in the root directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# connect_args={"check_same_thread": False} is needed only for SQLite.
# It allows FastAPI to access the database from multiple threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class to create our SQLAlchemy models.
Base = declarative_base()

# Dependency to get a database session for each request.
# It ensures the connection is closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
