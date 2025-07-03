from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class TemplateBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    template_content: str = Field(..., min_length=1)
    category: str = Field(..., max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    difficulty_level: str = Field(default="beginner", max_length=20)


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    template_content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    difficulty_level: Optional[str] = Field(None, max_length=20)
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None


class TemplateResponse(TemplateBase):
    id: int
    usage_count: int
    average_rating: float
    rating_count: int
    is_public: bool
    is_featured: bool
    estimated_tokens: Optional[int] = None
    optimization_potential: Optional[float] = None
    author: Optional[str] = None
    version: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TemplateList(BaseModel):
    templates: List[TemplateResponse]
    total: int
    page: int
    limit: int 