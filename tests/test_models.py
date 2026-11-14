from sqlalchemy import inspect
from app.models.listing import Listing
from app.models.category import Category, Subcategory
from app.models.seller import Seller


def test_listing_model_columns():
    inspector = inspect(Listing)
    column_names = {col.key for col in inspector.columns}

    # Verify all required columns exist in Listing model:
    required_columns = {
        "id",
        "slug",
        "seller_id",
        "subcategory_id",
        "title",
        "description",
        "price",
        "file_name",
        "file_url",
        "file_size",
        "created_at",
        "updated_at",
    }
    assert required_columns.issubset(column_names), f"Missing columns: {required_columns - column_names}"

    # Verify ID is primary key and integer
    id_col = inspector.columns["id"]
    assert id_col.primary_key is True
    assert id_col.type.python_type is int

    # Verify slug is unique and indexed
    slug_col = inspector.columns["slug"]
    assert slug_col.unique is True
    assert slug_col.index is True
    assert slug_col.nullable is False


def test_database_relationships_use_integer_id(db_session):
    cat = Category(name="Electronics")
    db_session.add(cat)
    db_session.commit()
    assert isinstance(cat.id, int)

    sub = Subcategory(name="Laptops", category_id=cat.id)
    db_session.add(sub)
    db_session.commit()
    assert isinstance(sub.id, int)
    assert sub.category.id == cat.id

    seller = Seller(name="SuperSeller")
    db_session.add(seller)
    db_session.commit()
    assert isinstance(seller.id, int)

    listing = Listing(
        slug="thinkpad-x1",
        seller_id=seller.id,
        subcategory_id=sub.id,
        title="Thinkpad X1",
        description="Laptop",
        price=1500.0,
        file_name="spec.pdf",
        file_url="/files/spec.pdf",
        file_size=1048576,
    )
    db_session.add(listing)
    db_session.commit()

    # Verify primary key is integer
    assert isinstance(listing.id, int)
    # Verify relationships resolve using integer foreign keys
    assert listing.seller.id == seller.id
    assert listing.subcategory.id == sub.id
    assert listing.category.id == cat.id
