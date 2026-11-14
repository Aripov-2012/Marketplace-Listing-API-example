import re
import unicodedata
from typing import Optional
from sqlalchemy.orm import Session

# Regex pattern for a valid public slug:
# Only lowercase alphanumeric characters and single hyphens, no consecutive hyphens, no leading/trailing hyphens.
SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Transliteration mapping for Cyrillic scripts (e.g. Uzbek Cyrillic / Russian)
CYRILLIC_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "",
    "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o", "қ": "q",
    "ғ": "g", "ҳ": "h",
}


def is_valid_slug(slug: str) -> bool:
    """Validate whether the given string is a valid slug format."""
    if not slug or not isinstance(slug, str):
        return False
    return bool(SLUG_REGEX.match(slug))


def slugify(text: str) -> str:
    """
    Convert a title or string into a URL-friendly slug.
    Special handling:
    - Uzbek apostrophes (', `, ʻ, ʼ, ‘, ’) inside words are removed so that
      "Noto'g'ri fe'llar jadvali" becomes "notogri-fellar-jadvali".
    - Cyrillic letters are transliterated.
    - Accents are removed via NFKD normalization.
    - All non-alphanumeric characters become hyphens.
    - Consecutive hyphens are collapsed and edge hyphens are stripped.
    """
    if not text:
        return ""

    # Strip apostrophes / modifier letters within words (e.g., o', g', fe'llar)
    text = re.sub(r"[\x27\x60\u02bb\u02bc\u2018\u2019]", "", text)

    # Transliterate Cyrillic characters
    for cyr, lat in CYRILLIC_MAP.items():
        text = text.replace(cyr, lat).replace(cyr.upper(), lat)

    # Normalize unicode to remove diacritics
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    text = text.lower()

    # Replace any non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    return text


def generate_unique_slug(base_text: str, db: Session, current_id: Optional[int] = None) -> str:
    """
    Generate a unique slug for a listing.
    If the base slug already exists in the database, appends -2, -3, etc.
    """
    from app.models.listing import Listing

    base_slug = slugify(base_text)
    if not base_slug:
        base_slug = "listing"

    # Query all matching slugs starting with base_slug to efficiently find next suffix
    query = db.query(Listing.slug).filter(
        (Listing.slug == base_slug) | (Listing.slug.like(f"{base_slug}-%"))
    )
    if current_id is not None:
        query = query.filter(Listing.id != current_id)

    existing_slugs = {row[0] for row in query.all()}

    if base_slug not in existing_slugs:
        return base_slug

    counter = 2
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1

    return f"{base_slug}-{counter}"
