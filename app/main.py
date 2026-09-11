# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import books

# Automatically create tables in the SQLite database.
# Note: For production use cases, using a migration tool like Alembic is recommended.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore Inventory Management System",
    description="A CRUD backend API designed for beginner developer interviews.",
    version="1.0.0",
)

# Register endpoints from books router
app.include_router(books.router)

@app.get("/")
def read_root():
    """
    Root endpoint showing api metadata.
    """
    return {
        "message": "Welcome to the Bookstore Inventory Management API",
        "docs_url": "/docs",
        "status": "healthy"
    }
