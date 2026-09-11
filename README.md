# Bookstore Inventory Management & Catalog API ⚙️

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=flat-square)](https://docs.pydantic.dev)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passing-brightgreen?style=flat-square)](https://pytest.org)

A modular, production-ready RESTful CRUD API built with **FastAPI**, **SQLAlchemy ORM (2.0)**, and **SQLite/PostgreSQL**.

Designed with clean architecture principles, featuring strict request/response data validation, centralized database dependency injection, comprehensive unit and integration test coverage, and automated OpenAPI documentation.

---

## 🌟 Architecture & Features

- **Layered Clean Architecture:** Strict separation of concerns across Routers, Schemas, CRUD handlers, and ORM Models.
- **Data Validation & Serialization:** Powered by Pydantic V2 schemas ensuring strict type-safety, constraint enforcement, and automatic serialization.
- **Database Abstraction:** SQLAlchemy 2.0 with decoupled session management and clean dependency injection (get_db).
- **Interactive Documentation:** Fully typed Swagger UI automatically available at /docs and ReDoc at /redoc.
- **Automated Test Suite:** Robust test suite with isolated in-memory test database fixtures using Pytest and HTTPX TestClient.

---

## 📁 Directory Structure

`	ext
PythonBackend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application factory & router mounting
│   ├── database.py      # Engine configuration & get_db dependency injection
│   ├── models.py        # SQLAlchemy relational database models
│   ├── schemas.py       # Pydantic request/response validation schemas
│   ├── crud.py          # Database operations (CREATE, READ, UPDATE, DELETE)
│   └── routers/
│       ├── __init__.py
│       └── books.py     # Books REST endpoint router
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures (isolated in-memory DB, TestClient)
│   └── test_books.py    # Unit & integration endpoint tests
├── requirements.txt     # Locked production dependencies
└── README.md            # Technical documentation
`

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10+ installed

### 2. Environment Setup

`ash
# Clone the repository
git clone https://github.com/adityanyadav1602/PythonBackend.git
cd PythonBackend

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
`

### 3. Run the API Server

`ash
uvicorn app.main:app --reload
`

Once started, access the interactive API docs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Automated Tests

Run the full Pytest test suite with coverage:

`ash
pytest -v
`

All tests execute against an isolated in-memory SQLite database, guaranteeing zero side-effects on development data.

---

## 📖 REST API Endpoints

| Method | Endpoint | Description | Request Body / Params | Response Codes |
| :--- | :--- | :--- | :--- | :--- |
| GET | / | Health check & API status | None | 200 OK |
| GET | /books/ | List all books (Paginated) | skip (int), limit (int) | 200 OK |
| POST | /books/ | Create a new book record | JSON payload (BookCreate) | 201 Created, 400 Bad Request, 422 Unprocessable |
| GET | /books/{id} | Retrieve book details | ook_id (int) | 200 OK, 404 Not Found |
| PUT | /books/{id} | Update book record (Partial) | JSON payload (BookUpdate) | 200 OK, 400 Bad Request, 404 Not Found |
| DELETE | /books/{id} | Remove book from inventory | ook_id (int) | 200 OK, 404 Not Found |

---

## 👤 Author

- **Aditya N. Yadav**
- Email: [aditya.n.yadav.dev@gmail.com](mailto:aditya.n.yadav.dev@gmail.com)
- LinkedIn: [aditya-narayanyadav](https://www.linkedin.com/in/aditya-narayanyadav/)
- GitHub: [@adityanyadav1602](https://github.com/adityanyadav1602)
