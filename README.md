# Bookstore Inventory Management API

This is a clean, production-ready RESTful CRUD API built with **FastAPI**, **SQLAlchemy ORM**, and **SQLite**. It has been designed specifically as a starting point for backend developer coding interviews (juniors/beginners).

---

## Technical Stack
- **Web Framework**: FastAPI (provides interactive `/docs` Swagger UI)
- **Database**: SQLite (local, file-based, zero setup required)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Testing**: Pytest (uses an isolated in-memory SQLite database)

---

## Directory Structure
```text
PythonBackend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & router registration
│   ├── database.py      # SQLite connection & get_db dependency injection
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic validation schemas
│   ├── crud.py          # Database operations (CREATE, READ, UPDATE, DELETE)
│   └── routers/
│       ├── __init__.py
│       └── books.py     # Books REST endpoint router
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures (DB isolation, TestClient)
│   └── test_books.py    # Unit & integration endpoint tests
├── requirements.txt     # Python dependencies
└── README.md            # Running instructions & interview exercises
```

---

## Setup & Running Guide

### Prerequisites
- Python 3.10 or higher installed.

### 1. Create a Virtual Environment
From the root directory:
```powershell
python -m venv .venv
```

### 2. Activate the Virtual Environment
- **On Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **On Windows (CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **On macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API Server
```bash
uvicorn app.main:app --reload
```
Once the server starts, you can visit the interactive API documentation at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** (Swagger UI)

### 5. Run the Test Suite
Ensure tests run and pass to verify your setup:
```bash
pytest
```

---

## REST API Documentation

| Method | Endpoint | Description | Request Body / Parameters | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | API Status & Welcome | None | `200 OK` |
| **GET** | `/books/` | List all books (Paginated) | `skip` (int, default=0), `limit` (int, default=100) | `200 OK` |
| **POST** | `/books/` | Create a new book | JSON: Book details (validated fields) | `201 Created`, `400 Bad Request` (Duplicate ISBN), `422 Unprocessable Entity` (Validation failure) |
| **GET** | `/books/{book_id}` | Retrieve a specific book | `book_id` (path parameter) | `200 OK`, `404 Not Found` |
| **PUT** | `/books/{book_id}` | Update book details (Partial update) | JSON: Book fields to update (optional) | `200 OK`, `400 Bad Request` (ISBN Conflict), `404 Not Found` |
| **DELETE**| `/books/{book_id}` | Delete a book record | `book_id` (path parameter) | `200 OK`, `404 Not Found` |

---

## 🎯 Interview Coding Exercises (Beginner/Junior Level)

Here are structured exercises that can be assigned to the candidate during a live-coding session or as a take-home assignment:

### Exercise 1: Model Expansion (Easy)
**Goal**: Add a `genre` field (representing the category of the book) to the inventory.
1. Modify `app/models.py` to add a `genre` column (string, nullable=True).
2. Update Pydantic schemas in `app/schemas.py`:
   - Add `genre` (optional string) to `BookBase`, `BookCreate`, `BookUpdate`, and `Book`.
3. Modify `app/crud.py` to ensure `genre` is saved when creating a book.
4. Verify the Swagger documentation at `/docs` reflects the new field.

### Exercise 2: Input Validation (Easy)
**Goal**: Enforce business rules around the publication year.
1. Modify the validation in `app/schemas.py` to ensure that `published_year` is not in the future (i.e., it must be less than or equal to the current year).
2. *Hint*: You can use a custom validator (`@field_validator` in Pydantic v2) to dynamically validate against `datetime.date.today().year`.

### Exercise 3: Filter & Search (Medium)
**Goal**: Allow users to filter books by author or title.
1. Modify `GET /books/` route in `app/routers/books.py` to accept optional query parameters: `author: Optional[str] = None` and `search: Optional[str] = None`.
2. Update `app/crud.py`'s `get_books()` function to filter database queries:
   - If `author` is provided, filter by exact matches or case-insensitive matches.
   - If `search` is provided, perform a case-insensitive search (substring match) on the `title` field.

### Exercise 4: Automated Testing (Medium)
**Goal**: Demonstrate testing principles.
1. Write a new test inside `tests/test_books.py` called `test_create_book_future_year()` to verify that creating a book with a future publication year throws a `422 Unprocessable Entity` status code (relates to Exercise 2).
2. Write a test to assert that searching/filtering by author works correctly and returns only the matched book (relates to Exercise 3).
