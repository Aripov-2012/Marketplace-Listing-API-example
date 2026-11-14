from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from app.schemas.category import CategoryResponse, SubcategoryResponse
from app.services.slug import is_valid_slug


class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0
    seller_id: int
    subcategory_id: int
    file_name: str
    file_url: str
    file_size: int


class ListingCreate(ListingBase):
    slug: Optional[str] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not is_valid_slug(v):
                raise ValueError(
                    "Invalid slug format. Slug must consist of lowercase letters, numbers, and single hyphens."
                )
        return v


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    seller_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    slug: Optional[str] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not is_valid_slug(v):
                raise ValueError(
                    "Invalid slug format. Slug must consist of lowercase letters, numbers, and single hyphens."
                )
        return v


class ListingResponse(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    price: Union[int, float]
    seller_id: int
    category: Optional[CategoryResponse] = None
    subcategory: Optional[SubcategoryResponse] = None
    file_name: str
    file_url: str
    file_size: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def serialize_price(self, v: float):
        if isinstance(v, (int, float)) and v == int(v):
            return int(v)
        return v
