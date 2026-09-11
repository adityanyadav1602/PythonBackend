import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# In-memory SQLite database connection URL for isolated tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# StaticPool is used to share the same in-memory database connection
# across all connections within a test execution.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def fixture_db_session():
    """
    Creates and populates database tables before each test runs,
    yields the session, and drops all tables after the test finishes.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def fixture_client(db_session):
    """
    Yields a FastAPI TestClient configured to use the temporary test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override get_db in FastAPI app dependencies
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # Clear overrides to prevent leaking database state to other tests
    app.dependency_overrides.clear()
