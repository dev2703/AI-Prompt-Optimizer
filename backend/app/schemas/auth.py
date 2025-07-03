from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import SubscriptionTier


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_tier: SubscriptionTier
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: "User"


class TokenData(BaseModel):
    email: Optional[str] = None


# Import User schema to avoid circular imports
from app.schemas.user import User
Token.model_rebuild() 