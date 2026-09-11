def test_read_root(client):
    """
    Test that the root endpoint returns a status 200 and details.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["docs_url"] == "/docs"

def test_create_book(client):
    """
    Test successful creation of a book.
    """
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "price": 35.99,
        "quantity": 10,
        "published_year": 2008
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert data["price"] == book_data["price"]
    assert data["quantity"] == book_data["quantity"]
    assert data["published_year"] == book_data["published_year"]
    assert "id" in data

def test_create_book_duplicate_isbn(client):
    """
    Test that creating a book with a duplicate ISBN raises a 400 Bad Request error.
    """
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "price": 35.99,
        "quantity": 10,
        "published_year": 2008
    }
    # Create first book
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    
    # Try creating second book with duplicate ISBN
    response = client.post("/books/", json=book_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Book with this ISBN already exists."

def test_create_book_invalid_price(client):
    """
    Test Pydantic validation: non-negative check on book price.
    """
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "price": -5.0,  # Invalid negative price
        "quantity": 10,
        "published_year": 2008
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(err["loc"] == ["body", "price"] for err in errors)

def test_create_book_invalid_quantity(client):
    """
    Test Pydantic validation: non-negative check on quantity.
    """
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "price": 35.99,
        "quantity": -1,  # Invalid negative quantity
        "published_year": 2008
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(err["loc"] == ["body", "quantity"] for err in errors)

def test_read_book(client):
    """
    Test retrieving a specific book by ID.
    """
    book_data = {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "isbn": "9780135957059",
        "price": 42.50,
        "quantity": 5,
        "published_year": 2019
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    
    # Get the book
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["isbn"] == book_data["isbn"]

def test_read_book_not_found(client):
    """
    Test that retrieving a non-existent book ID returns a 404 error.
    """
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_read_books_list(client):
    """
    Test retrieving a list of all books.
    """
    books_to_create = [
        {"title": "Book A", "author": "Author A", "isbn": "1111111111", "price": 10.00, "quantity": 1, "published_year": 2000},
        {"title": "Book B", "author": "Author B", "isbn": "2222222222", "price": 20.00, "quantity": 2, "published_year": 2005}
    ]
    for b in books_to_create:
        client.post("/books/", json=b)
        
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book A"
    assert data[1]["title"] == "Book B"

def test_update_book(client):
    """
    Test updating a book's details.
    """
    book_data = {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": "9780134757599",
        "price": 45.00,
        "quantity": 3,
        "published_year": 2018
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    
    # Partially update price and quantity
    update_data = {
        "price": 39.99,
        "quantity": 8
    }
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 39.99
    assert data["quantity"] == 8
    assert data["title"] == "Refactoring"  # Unchanged field remains the same

def test_update_book_isbn_conflict(client):
    """
    Test that updating a book's ISBN to an already existing ISBN of another book raises 400.
    """
    # Create Book 1
    client.post("/books/", json={"title": "Book 1", "author": "Author 1", "isbn": "1111111111", "price": 10.0, "quantity": 1, "published_year": 2000})
    # Create Book 2
    create_res = client.post("/books/", json={"title": "Book 2", "author": "Author 2", "isbn": "2222222222", "price": 20.0, "quantity": 2, "published_year": 2005})
    book_2_id = create_res.json()["id"]
    
    # Try updating Book 2 to use Book 1's ISBN
    response = client.put(f"/books/{book_2_id}", json={"isbn": "1111111111"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Another book with this ISBN already exists."

def test_update_book_not_found(client):
    """
    Test updating a non-existent book returns a 404 error.
    """
    response = client.put("/books/9999", json={"title": "Random"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_delete_book(client):
    """
    Test successful deletion of a book and subsequent 404 when querying.
    """
    book_data = {
        "title": "Design Patterns",
        "author": "Gang of Four",
        "isbn": "9780201633610",
        "price": 50.00,
        "quantity": 2,
        "published_year": 1994
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    
    # Delete the book
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    
    # Read book again to confirm deletion
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404

def test_delete_book_not_found(client):
    """
    Test deleting a non-existent book returns 404.
    """
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
