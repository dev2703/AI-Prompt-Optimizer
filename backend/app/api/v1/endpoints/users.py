from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.user import UserProfile, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user profile
    """
    return UserProfile.from_orm(current_user)


@router.put("/me", response_model=UserProfile)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update current user profile
    """
    # Update fields
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return UserProfile.from_orm(current_user)


@router.get("/me/usage")
async def get_user_usage(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user usage statistics
    """
    return {
        "subscription_tier": current_user.subscription_tier,
        "monthly_optimizations": current_user.monthly_optimizations,
        "optimizations_used": current_user.optimizations_used,
        "optimizations_remaining": current_user.optimizations_remaining,
        "monthly_tokens": current_user.monthly_tokens,
        "tokens_used": current_user.tokens_used,
        "tokens_remaining": current_user.tokens_remaining,
        "usage_percentage": {
            "optimizations": (current_user.optimizations_used / current_user.monthly_optimizations) * 100,
            "tokens": (current_user.tokens_used / current_user.monthly_tokens) * 100
        }
    }


@router.post("/me/reset-usage")
async def reset_user_usage(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Reset user usage (admin only or for testing)
    """
    # This would typically be called by a scheduled task
    # For now, we'll allow manual reset for testing
    current_user.optimizations_used = 0
    current_user.tokens_used = 0
    
    db.commit()
    
    return {"message": "Usage reset successfully"} 