from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.listing import Listing
from app.models.category import Subcategory
from app.models.seller import Seller
from app.schemas.listing import ListingCreate, ListingUpdate, ListingResponse
from app.services.slug import generate_unique_slug, is_valid_slug

router = APIRouter()


@router.get("", response_model=List[ListingResponse])
def get_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    subcategory_id: Optional[int] = None,
    seller_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Get all listings.
    Internal database ID is omitted; public identifier is slug.
    """
    query = db.query(Listing)
    if subcategory_id is not None:
        query = query.filter(Listing.subcategory_id == subcategory_id)
    if seller_id is not None:
        query = query.filter(Listing.seller_id == seller_id)

    listings = query.offset(skip).limit(limit).all()
    return listings


@router.get("/{slug}", response_model=ListingResponse)
def get_listing(
    slug: str,
    db: Session = Depends(get_db),
):
    """
    Get single listing details by its public slug.
    """
    listing = db.query(Listing).filter(Listing.slug == slug).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Listing with slug '{slug}' not found",
        )
    return listing


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
    listing_in: ListingCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new listing.
    Automatically generates unique slug from the title if not explicitly provided.
    If slug exists, appends numeric suffix.
    """
    # Verify subcategory exists
    subcategory = db.query(Subcategory).filter(Subcategory.id == listing_in.subcategory_id).first()
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subcategory with id {listing_in.subcategory_id} does not exist",
        )

    # Verify seller exists (or auto-create if needed for testing convenience)
    seller = db.query(Seller).filter(Seller.id == listing_in.seller_id).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Seller with id {listing_in.seller_id} does not exist",
        )

    # Determine unique slug
    if listing_in.slug:
        if not is_valid_slug(listing_in.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid slug format. Slug must consist of lowercase letters, numbers, and single hyphens.",
            )
        slug = generate_unique_slug(listing_in.slug, db)
    else:
        slug = generate_unique_slug(listing_in.title, db)

    listing_data = listing_in.model_dump(exclude={"slug"})
    listing = Listing(**listing_data, slug=slug)

    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.patch("/{slug}", response_model=ListingResponse)
def update_listing(
    slug: str,
    listing_in: ListingUpdate,
    db: Session = Depends(get_db),
):
    """
    Update listing by its public slug.
    - Slug is updated only when explicitly provided in the request body.
    - Title updates DO NOT automatically change the existing slug.
    - Slug format is validated.
    - Slug uniqueness is enforced.
    """
    listing = db.query(Listing).filter(Listing.slug == slug).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Listing with slug '{slug}' not found",
        )

    update_data = listing_in.model_dump(exclude_unset=True)

    # If subcategory_id is being updated, verify it exists
    if "subcategory_id" in update_data:
        subcategory = db.query(Subcategory).filter(Subcategory.id == update_data["subcategory_id"]).first()
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subcategory with id {update_data['subcategory_id']} does not exist",
            )

    # If seller_id is being updated, verify it exists
    if "seller_id" in update_data:
        seller = db.query(Seller).filter(Seller.id == update_data["seller_id"]).first()
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seller with id {update_data['seller_id']} does not exist",
            )

    # Handle explicit slug update
    if "slug" in update_data:
        new_slug = update_data["slug"]
        if not is_valid_slug(new_slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid slug format. Slug must consist of lowercase letters, numbers, and single hyphens.",
            )
        # Check uniqueness against other listings
        existing = db.query(Listing).filter(
            Listing.slug == new_slug,
            Listing.id != listing.id,
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slug '{new_slug}' already exists",
            )
        listing.slug = new_slug

    # Update other fields without touching slug
    for field, value in update_data.items():
        if field != "slug":
            setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return listing
