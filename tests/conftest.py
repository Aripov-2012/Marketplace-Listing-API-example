import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.models.category import Category, Subcategory
from app.models.seller import Seller
from app.main import app

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Seed default category, subcategory and seller matching user prompt example:
    # Category: id=1, name="Amaliy ishlar"
    # Subcategory: id=3, name="Ingliz tili"
    # Seller: id=1
    category = Category(id=1, name="Amaliy ishlar")
    subcategory = Subcategory(id=3, category_id=1, name="Ingliz tili")
    seller = Seller(id=1, name="Test Seller")

    session.add(category)
    session.add(subcategory)
    session.add(seller)
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
