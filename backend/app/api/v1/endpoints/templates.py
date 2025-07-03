from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateResponse, TemplateList

router = APIRouter()


@router.get("/", response_model=List[TemplateResponse])
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    industry: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    is_featured: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get available templates with optional filtering
    """
    query = db.query(Template).filter(Template.is_public == True)
    
    if category:
        query = query.filter(Template.category == category)
    if industry:
        query = query.filter(Template.industry == industry)
    if difficulty_level:
        query = query.filter(Template.difficulty_level == difficulty_level)
    if is_featured is not None:
        query = query.filter(Template.is_featured == is_featured)
    
    templates = query.order_by(Template.usage_count.desc()).offset(skip).limit(limit).all()
    return [TemplateResponse.from_orm(template) for template in templates]


@router.get("/categories")
async def get_template_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get available template categories
    """
    categories = db.query(Template.category).distinct().all()
    return [category[0] for category in categories if category[0]]


@router.get("/industries")
async def get_template_industries(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get available template industries
    """
    industries = db.query(Template.industry).distinct().all()
    return [industry[0] for industry in industries if industry[0]]


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific template by ID
    """
    template = db.query(Template).filter(Template.id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    if not template.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Template not accessible"
        )
    
    # Increment usage count
    template.increment_usage()
    db.commit()
    
    return TemplateResponse.from_orm(template)


@router.post("/{template_id}/rate")
async def rate_template(
    template_id: int,
    rating: float,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Rate a template (1-5 stars)
    """
    if not 1 <= rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    template = db.query(Template).filter(Template.id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    template.add_rating(rating)
    db.commit()
    
    return {"message": "Rating submitted successfully"}


@router.get("/featured", response_model=List[TemplateResponse])
async def get_featured_templates(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get featured templates
    """
    templates = db.query(Template).filter(
        Template.is_public == True,
        Template.is_featured == True
    ).order_by(Template.usage_count.desc()).limit(limit).all()
    
    return [TemplateResponse.from_orm(template) for template in templates] 