from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.prompt import Prompt, Optimization, OptimizationType
from app.schemas.prompt import OptimizationRequest, OptimizationResponse
from app.services.optimization_service import OptimizationService
from app.services.token_service import TokenService
from app.tasks.optimization_tasks import optimize_prompt_task

router = APIRouter()


@router.post("/", response_model=OptimizationResponse)
async def optimize_prompt(
    optimization_request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Optimize a prompt using AI
    """
    # Check user limits
    estimated_tokens = len(optimization_request.original_prompt.split()) * 1.3  # Rough estimate
    if not current_user.can_optimize(int(estimated_tokens)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Optimization limit reached. Please upgrade your plan."
        )
    
    # Get or create prompt
    if optimization_request.prompt_id:
        prompt = db.query(Prompt).filter(
            Prompt.id == optimization_request.prompt_id,
            Prompt.user_id == current_user.id
        ).first()
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prompt not found"
            )
    else:
        # Create new prompt
        prompt = Prompt(
            user_id=current_user.id,
            original_prompt=optimization_request.original_prompt,
            status="draft"
        )
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
    
    # Start optimization in background
    task = optimize_prompt_task.delay(
        prompt_id=prompt.id,
        user_id=current_user.id,
        optimization_type=optimization_request.optimization_type,
        target_model=optimization_request.target_model,
        reduction_target=optimization_request.reduction_target,
        quality_threshold=optimization_request.quality_threshold
    )
    
    # Return immediate response with task ID
    return {
        "task_id": task.id,
        "status": "processing",
        "message": "Optimization started. Check task status for results."
    }


@router.get("/task/{task_id}")
async def get_optimization_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get optimization task status
    """
    from app.core.celery_app import celery_app
    
    task_result = celery_app.AsyncResult(task_id)
    
    if task_result.ready():
        if task_result.successful():
            result = task_result.result
            return {
                "status": "completed",
                "result": result
            }
        else:
            return {
                "status": "failed",
                "error": str(task_result.info)
            }
    else:
        return {
            "status": "processing",
            "task_id": task_id
        }


@router.get("/", response_model=List[OptimizationResponse])
async def get_optimizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    optimization_type: Optional[OptimizationType] = None,
    model_used: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user's optimization history
    """
    query = db.query(Optimization).filter(Optimization.user_id == current_user.id)
    
    if optimization_type:
        query = query.filter(Optimization.optimization_type == optimization_type)
    if model_used:
        query = query.filter(Optimization.model_used == model_used)
    
    optimizations = query.order_by(Optimization.created_at.desc()).offset(skip).limit(limit).all()
    return [OptimizationResponse.from_orm(opt) for opt in optimizations]


@router.get("/{optimization_id}", response_model=OptimizationResponse)
async def get_optimization(
    optimization_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific optimization by ID
    """
    optimization = db.query(Optimization).filter(
        Optimization.id == optimization_id,
        Optimization.user_id == current_user.id
    ).first()
    
    if not optimization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimization not found"
        )
    
    return OptimizationResponse.from_orm(optimization)


@router.post("/calculate-tokens")
async def calculate_tokens(
    text: str,
    model: str = "gpt-4",
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Calculate token count and estimated cost for a text
    """
    token_service = TokenService()
    token_count = token_service.count_tokens(text, model)
    estimated_cost = token_service.calculate_cost(token_count, model)
    
    return {
        "text_length": len(text),
        "token_count": token_count,
        "model": model,
        "estimated_cost": estimated_cost
    }


@router.post("/compare-models")
async def compare_models(
    text: str,
    models: List[str] = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Compare token count and cost across different models
    """
    token_service = TokenService()
    comparison = []
    
    for model in models:
        token_count = token_service.count_tokens(text, model)
        cost = token_service.calculate_cost(token_count, model)
        comparison.append({
            "model": model,
            "token_count": token_count,
            "estimated_cost": cost
        })
    
    return {
        "text_length": len(text),
        "comparison": comparison
    }


@router.delete("/{optimization_id}")
async def delete_optimization(
    optimization_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Delete an optimization
    """
    optimization = db.query(Optimization).filter(
        Optimization.id == optimization_id,
        Optimization.user_id == current_user.id
    ).first()
    
    if not optimization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimization not found"
        )
    
    db.delete(optimization)
    db.commit()
    
    return {"message": "Optimization deleted successfully"} 