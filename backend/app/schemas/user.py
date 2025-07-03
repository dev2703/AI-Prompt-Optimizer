from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import SubscriptionTier


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase):
    id: int
    subscription_tier: SubscriptionTier
    is_active: bool
    optimizations_remaining: int
    tokens_remaining: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserProfile(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_tier: SubscriptionTier
    is_active: bool
    optimizations_remaining: int
    tokens_remaining: int
    monthly_optimizations: int
    monthly_tokens: int
    optimizations_used: int
    tokens_used: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True 