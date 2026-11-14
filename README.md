# Listing API - Slug Architecture

This project implements the Listing API architecture using **`slug`** as the public identifier for listings instead of internal database IDs, built with FastAPI, SQLAlchemy 2.0, and Pydantic v2.

---

## 1. Features & Architecture

### Listing Model
- Internal Database Primary Key: `id` (Integer, primary key, internal use only).
- Public Identifier: `slug` (String, required, unique, indexed).
- Complete Listing Model attributes:
  - `id`: Integer (PK)
  - `slug`: String(255), unique, indexed, non-nullable
  - `seller_id`: Integer, ForeignKey("sellers.id")
  - `subcategory_id`: Integer, ForeignKey("subcategories.id")
  - `title`: String(255), non-nullable
  - `description`: Text, nullable
  - `price`: Float, non-nullable, default 0.0
  - `file_name`: String(255), non-nullable
  - `file_url`: String(500), non-nullable
  - `file_size`: Integer, non-nullable
  - `created_at`: DateTime (UTC)
  - `updated_at`: DateTime (UTC)

### Relational Integrity
- Database relationships and foreign keys continue using internal integer IDs (`sellers.id`, `subcategories.id`, `categories.id`).
- Category is dynamically resolved through the subcategory relationship (`listing.subcategory.category`).
- Public responses expose `slug` as the listing identifier and completely hide the internal database `id`.

### Slug Generation & Rules
- Automatic slug generation from `title` during listing creation (`POST /api/v1/listings`).
- Automatic transliteration and removal of Uzbek apostrophes / modifier letters (`'`, `ʻ`, `’`, `‘`, `` ` ``) so that `Noto'g'ri fe'llar jadvali` cleanly becomes `notogri-fellar-jadvali`.
- Uniqueness is strictly guaranteed: if a slug already exists, numeric suffixes are appended (`-2`, `-3`, etc.).
- `PATCH /api/v1/listings/{slug}` allows explicit slug updates when `slug` is provided in the request body.
- When `title` is updated via PATCH without providing `slug`, the existing slug is **not** automatically changed.
- Slug format validation enforces lowercase alphanumeric characters with single hyphens (`^[a-z0-9]+(?:-[a-z0-9]+)*$`).

---

## 2. API Endpoints

All public listing detail and update routes use `slug` instead of integer IDs:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/listings` | Retrieve all listings (returns list with `slug`, no internal `id`) |
| `GET` | `/api/v1/listings/{slug}` | Retrieve single listing by its public `slug` |
| `POST` | `/api/v1/listings` | Create new listing (auto-generates unique `slug`) |
| `PATCH` | `/api/v1/listings/{slug}` | Update listing by `slug` (explicit slug update supported, title update preserves slug) |

> **Note**: No `DELETE` endpoint is exposed (`DELETE /api/v1/listings/{slug}` returns `405 Method Not Allowed`).

---

## 3. Example Response

`GET /api/v1/listings/notogri-fellar-jadvali`

```json
{
  "slug": "notogri-fellar-jadvali",
  "title": "Noto'g'ri fe'llar jadvali",
  "description": "English irregular verbs",
  "price": 0,
  "seller_id": 1,
  "category": {
    "id": 1,
    "name": "Amaliy ishlar"
  },
  "subcategory": {
    "id": 3,
    "name": "Ingliz tili"
  },
  "file_name": "verbs.docx",
  "file_url": "/files/verbs.docx",
  "file_size": 32092
}
```

---

## 4. Setup & Running

### 1. Activate Virtual Environment
```bash
source "/home/aripov-abdulaziz/Рабочий стол/API/.venv/bin/activate"
```

### 2. Seed Database
```bash
python seed.py
```

### 3. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive API docs will be available at: `http://localhost:8000/docs`

### 4. Run Test Suite
```bash
pytest -v
```
