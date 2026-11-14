import pytest


def test_post_listing_auto_slug_generation(client):
    payload = {
        "title": "Noto'g'ri fe'llar jadvali",
        "description": "English irregular verbs",
        "price": 0,
        "seller_id": 1,
        "subcategory_id": 3,
        "file_name": "verbs.docx",
        "file_url": "/files/verbs.docx",
        "file_size": 32092,
    }

    response = client.post("/api/v1/listings", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["slug"] == "notogri-fellar-jadvali"
    assert data["title"] == "Noto'g'ri fe'llar jadvali"
    assert data["description"] == "English irregular verbs"
    assert data["price"] == 0
    assert data["seller_id"] == 1
    assert data["category"] == {"id": 1, "name": "Amaliy ishlar"}
    assert data["subcategory"] == {"id": 3, "name": "Ingliz tili"}
    assert data["file_name"] == "verbs.docx"
    assert data["file_url"] == "/files/verbs.docx"
    assert data["file_size"] == 32092

    # Internal database ID must NOT be exposed
    assert "id" not in data


def test_post_listing_duplicate_title_slug_suffix(client):
    payload = {
        "title": "Noto'g'ri fe'llar jadvali",
        "description": "First listing",
        "price": 100,
        "seller_id": 1,
        "subcategory_id": 3,
        "file_name": "verbs.docx",
        "file_url": "/files/verbs.docx",
        "file_size": 32092,
    }

    # First POST
    res1 = client.post("/api/v1/listings", json=payload)
    assert res1.status_code == 201
    assert res1.json()["slug"] == "notogri-fellar-jadvali"

    # Second POST with identical title
    res2 = client.post("/api/v1/listings", json=payload)
    assert res2.status_code == 201
    assert res2.json()["slug"] == "notogri-fellar-jadvali-2"

    # Third POST with identical title
    res3 = client.post("/api/v1/listings", json=payload)
    assert res3.status_code == 201
    assert res3.json()["slug"] == "notogri-fellar-jadvali-3"


def test_get_listing_by_slug_matches_specification(client):
    # Create listing as in Section 4 example
    payload = {
        "title": "Noto'g'ri fe'llar jadvali",
        "description": "English irregular verbs",
        "price": 0,
        "seller_id": 1,
        "subcategory_id": 3,
        "file_name": "verbs.docx",
        "file_url": "/files/verbs.docx",
        "file_size": 32092,
    }
    client.post("/api/v1/listings", json=payload)

    # Retrieve by slug
    response = client.get("/api/v1/listings/notogri-fellar-jadvali")
    assert response.status_code == 200

    data = response.json()
    expected = {
        "slug": "notogri-fellar-jadvali",
        "title": "Noto'g'ri fe'llar jadvali",
        "description": "English irregular verbs",
        "price": 0,
        "seller_id": 1,
        "category": {
            "id": 1,
            "name": "Amaliy ishlar",
        },
        "subcategory": {
            "id": 3,
            "name": "Ingliz tili",
        },
        "file_name": "verbs.docx",
        "file_url": "/files/verbs.docx",
        "file_size": 32092,
    }
    assert data == expected
    assert "id" not in data


def test_get_listing_not_found(client):
    response = client.get("/api/v1/listings/non-existent-slug")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_all_listings(client):
    # Create two listings
    client.post(
        "/api/v1/listings",
        json={
            "title": "Listing 1",
            "price": 10,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "1.pdf",
            "file_url": "/1.pdf",
            "file_size": 1024,
        },
    )
    client.post(
        "/api/v1/listings",
        json={
            "title": "Listing 2",
            "price": 20,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "2.pdf",
            "file_url": "/2.pdf",
            "file_size": 2048,
        },
    )

    response = client.get("/api/v1/listings")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    for item in items:
        assert "slug" in item
        assert "id" not in item


def test_patch_title_does_not_change_slug(client):
    # Requirement: "Do not automatically change an existing slug when the title is updated."
    client.post(
        "/api/v1/listings",
        json={
            "title": "Initial Title",
            "price": 0,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "doc.pdf",
            "file_url": "/doc.pdf",
            "file_size": 500,
        },
    )

    # Slug should initially be 'initial-title'
    get_res = client.get("/api/v1/listings/initial-title")
    assert get_res.status_code == 200

    # PATCH title
    patch_res = client.patch(
        "/api/v1/listings/initial-title",
        json={"title": "Updated Brand New Title"},
    )
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["title"] == "Updated Brand New Title"
    # Slug must remain 'initial-title'!
    assert data["slug"] == "initial-title"

    # Verify listing is still reachable via original slug
    assert client.get("/api/v1/listings/initial-title").status_code == 200


def test_patch_slug_explicitly_updates_slug(client):
    # Requirement: "Allow the slug to be updated through PATCH when explicitly provided."
    client.post(
        "/api/v1/listings",
        json={
            "title": "Original Title",
            "price": 0,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "doc.pdf",
            "file_url": "/doc.pdf",
            "file_size": 500,
        },
    )

    patch_res = client.patch(
        "/api/v1/listings/original-title",
        json={"slug": "custom-new-slug"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["slug"] == "custom-new-slug"

    # Old slug should now 404
    assert client.get("/api/v1/listings/original-title").status_code == 404
    # New slug should retrieve it
    assert client.get("/api/v1/listings/custom-new-slug").status_code == 200


def test_patch_slug_duplicate_rejected(client):
    # Create two listings
    client.post(
        "/api/v1/listings",
        json={
            "title": "First",
            "price": 0,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "1.pdf",
            "file_url": "/1.pdf",
            "file_size": 500,
        },
    )
    client.post(
        "/api/v1/listings",
        json={
            "title": "Second",
            "price": 0,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "2.pdf",
            "file_url": "/2.pdf",
            "file_size": 500,
        },
    )

    # Attempt to rename "second" to "first"
    patch_res = client.patch(
        "/api/v1/listings/second",
        json={"slug": "first"},
    )
    assert patch_res.status_code == 400
    assert "already exists" in patch_res.json()["detail"].lower()


def test_patch_invalid_slug_format_rejected(client):
    client.post(
        "/api/v1/listings",
        json={
            "title": "Valid Listing",
            "price": 0,
            "seller_id": 1,
            "subcategory_id": 3,
            "file_name": "doc.pdf",
            "file_url": "/doc.pdf",
            "file_size": 500,
        },
    )

    # Try invalid formats (uppercase, spaces, leading hyphens, double hyphens)
    invalid_slugs = ["INVALID SLUG", "-leading-hyphen", "trailing-hyphen-", "double--hyphen", "special@char"]
    for inv in invalid_slugs:
        res = client.patch(
            "/api/v1/listings/valid-listing",
            json={"slug": inv},
        )
        assert res.status_code in (400, 422), f"Expected 400/422 for invalid slug '{inv}', got {res.status_code}"


def test_delete_endpoint_not_allowed(client):
    # Requirement: "Do not create a DELETE endpoint."
    res1 = client.delete("/api/v1/listings/some-slug")
    assert res1.status_code == 405  # Method Not Allowed

    res2 = client.delete("/api/v1/listings")
    assert res2.status_code == 405  # Method Not Allowed
