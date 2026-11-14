import pytest
from app.services.slug import slugify, is_valid_slug, generate_unique_slug
from app.models.listing import Listing


def test_slugify_uzbek_characters():
    # Prompt example:
    # Title: Noto'g'ri fe'llar jadvali -> notogri-fellar-jadvali
    title = "Noto'g'ri fe'llar jadvali"
    slug = slugify(title)
    assert slug == "notogri-fellar-jadvali"


def test_slugify_various_apostrophes():
    # Test different unicode apostrophes used in Uzbek:
    # ASCII quote: '
    # Modifier letter turned comma: ʻ
    # Right single quote: ’
    # Left single quote: ‘
    # Backtick: `
    variants = [
        "Noto'g'ri fe'llar jadvali",
        "Notoʻgʻri feʻllar jadvali",
        "Noto’g’ri fe’llar jadvali",
        "Noto‘g‘ri fe‘llar jadvali",
        "Noto`g`ri fe`llar jadvali",
    ]
    for variant in variants:
        assert slugify(variant) == "notogri-fellar-jadvali"


def test_is_valid_slug():
    # Valid slugs
    assert is_valid_slug("notogri-fellar-jadvali") is True
    assert is_valid_slug("notogri-fellar-jadvali-2") is True
    assert is_valid_slug("listing-100") is True
    assert is_valid_slug("abc") is True
    assert is_valid_slug("123") is True

    # Invalid slugs
    assert is_valid_slug("") is False
    assert is_valid_slug("Noto'g'ri") is False
    assert is_valid_slug("Invalid Slug") is False
    assert is_valid_slug("invalid_slug") is False
    assert is_valid_slug("-invalid") is False
    assert is_valid_slug("invalid-") is False
    assert is_valid_slug("invalid--slug") is False
    assert is_valid_slug("slug@test") is False


def test_generate_unique_slug_numeric_suffix(db_session):
    # Test prompt requirement:
    # "Title: Noto'g'ri fe'llar jadvali
    # Slug: notogri-fellar-jadvali
    # If the same slug already exists:
    # notogri-fellar-jadvali-2"
    title = "Noto'g'ri fe'llar jadvali"

    # First slug
    slug1 = generate_unique_slug(title, db_session)
    assert slug1 == "notogri-fellar-jadvali"

    # Add to DB
    l1 = Listing(
        slug=slug1,
        seller_id=1,
        subcategory_id=3,
        title=title,
        description="test",
        price=0,
        file_name="verbs.docx",
        file_url="/files/verbs.docx",
        file_size=32092,
    )
    db_session.add(l1)
    db_session.commit()

    # Second slug
    slug2 = generate_unique_slug(title, db_session)
    assert slug2 == "notogri-fellar-jadvali-2"

    l2 = Listing(
        slug=slug2,
        seller_id=1,
        subcategory_id=3,
        title=title,
        description="test 2",
        price=0,
        file_name="verbs.docx",
        file_url="/files/verbs.docx",
        file_size=32092,
    )
    db_session.add(l2)
    db_session.commit()

    # Third slug
    slug3 = generate_unique_slug(title, db_session)
    assert slug3 == "notogri-fellar-jadvali-3"


def test_generate_unique_slug_for_self_update(db_session):
    # When updating the same listing, its own slug should not conflict
    title = "Noto'g'ri fe'llar jadvali"
    slug1 = generate_unique_slug(title, db_session)

    l1 = Listing(
        slug=slug1,
        seller_id=1,
        subcategory_id=3,
        title=title,
        description="test",
        price=0,
        file_name="verbs.docx",
        file_url="/files/verbs.docx",
        file_size=32092,
    )
    db_session.add(l1)
    db_session.commit()

    # Exclude current listing ID
    slug_same = generate_unique_slug(title, db_session, current_id=l1.id)
    assert slug_same == "notogri-fellar-jadvali"
