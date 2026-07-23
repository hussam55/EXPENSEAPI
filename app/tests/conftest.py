import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your app and database components
from app.main import app
from app.db import get_db, Base

# 1. Create a temporary SQLite database specifically for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Pytest Fixture: This runs before every test to create clean tables
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine) # Create tables
    yield
    Base.metadata.drop_all(bind=engine)   # Destroy tables after tests finish

# 3. Pytest Fixture: This overrides FastAPI's normal database connection
@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    # Swap out the real database for the test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Return the simulated web browser
    with TestClient(app) as c:
        yield c