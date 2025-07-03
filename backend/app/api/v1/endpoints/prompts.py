from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.prompt import Prompt, PromptStatus
from app.schemas.prompt import PromptCreate, PromptUpdate, PromptResponse, PromptList

router = APIRouter()


@router.post("/", response_model=PromptResponse)
def create_prompt(
    prompt_data: PromptCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Create a new prompt
    """
    # Check user limits
    if not current_user.can_optimize():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Optimization limit reached. Please upgrade your plan."
        )
    
    db_prompt = Prompt(
        user_id=current_user.id,
        original_prompt=prompt_data.original_prompt,
        title=prompt_data.title,
        description=prompt_data.description,
        tags=prompt_data.tags,
        category=prompt_data.category,
        prompt_type=prompt_data.prompt_type
    )
    
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    
    return PromptResponse.from_orm(db_prompt)


@router.get("/", response_model=List[PromptResponse])
def get_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[PromptStatus] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user's prompts with optional filtering
    """
    query = db.query(Prompt).filter(Prompt.user_id == current_user.id)
    
    if status:
        query = query.filter(Prompt.status == status)
    if category:
        query = query.filter(Prompt.category == category)
    
    prompts = query.offset(skip).limit(limit).all()
    return [PromptResponse.from_orm(prompt) for prompt in prompts]


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific prompt by ID
    """
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    return PromptResponse.from_orm(prompt)


@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(
    prompt_id: int,
    prompt_data: PromptUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update a prompt
    """
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Update fields
    for field, value in prompt_data.dict(exclude_unset=True).items():
        setattr(prompt, field, value)
    
    db.commit()
    db.refresh(prompt)
    
    return PromptResponse.from_orm(prompt)


@router.delete("/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Delete a prompt
    """
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    db.delete(prompt)
    db.commit()
    
    return {"message": "Prompt deleted successfully"}


@router.get("/{prompt_id}/history", response_model=List[dict])
def get_prompt_history(
    prompt_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get optimization history for a prompt
    """
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Get optimization history
    optimizations = prompt.optimizations
    history = []
    
    for opt in optimizations:
        history.append({
            "id": opt.id,
            "optimization_type": opt.optimization_type,
            "model_used": opt.model_used,
            "token_reduction_percentage": opt.token_reduction_percentage,
            "quality_score": opt.quality_score,
            "cost_savings": opt.cost_savings,
            "created_at": opt.created_at
        })
    
    return history 