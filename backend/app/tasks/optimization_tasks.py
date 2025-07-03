from celery import current_task
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.services.optimization_service import OptimizationService
from app.models.user import User
from app.models.prompt import OptimizationType


@celery_app.task(bind=True)
def optimize_prompt_task(
    self,
    prompt_id: int,
    user_id: int,
    optimization_type: str,
    target_model: str = None,
    reduction_target: float = None,
    quality_threshold: float = None
):
    """
    Background task for prompt optimization
    """
    try:
        # Update task status
        current_task.update_state(
            state='PROGRESS',
            meta={'status': 'Starting optimization...'}
        )
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Initialize optimization service
            optimization_service = OptimizationService()
            
            # Update task status
            current_task.update_state(
                state='PROGRESS',
                meta={'status': 'Processing optimization...'}
            )
            
            # Perform optimization
            result = optimization_service.optimize_prompt(
                prompt_id=prompt_id,
                user_id=user_id,
                optimization_type=OptimizationType(optimization_type),
                target_model=target_model,
                reduction_target=reduction_target,
                quality_threshold=quality_threshold,
                db=db
            )
            
            # Update user usage
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                tokens_used = result.get('original_tokens', 0) + result.get('optimized_tokens', 0)
                user.record_optimization(tokens_used)
                db.commit()
            
            # Update task status
            current_task.update_state(
                state='SUCCESS',
                meta={
                    'status': 'Optimization completed successfully',
                    'result': result
                }
            )
            
            return result
            
        finally:
            db.close()
    
    except Exception as e:
        # Update task status with error
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Optimization failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def batch_optimize_prompts_task(
    self,
    prompt_ids: list,
    user_id: int,
    optimization_type: str,
    target_model: str = None
):
    """
    Background task for batch prompt optimization
    """
    try:
        results = []
        total_prompts = len(prompt_ids)
        
        for i, prompt_id in enumerate(prompt_ids):
            # Update task status
            current_task.update_state(
                state='PROGRESS',
                meta={
                    'status': f'Processing prompt {i+1}/{total_prompts}',
                    'progress': (i / total_prompts) * 100
                }
            )
            
            # Optimize individual prompt
            result = optimize_prompt_task.delay(
                prompt_id=prompt_id,
                user_id=user_id,
                optimization_type=optimization_type,
                target_model=target_model
            )
            
            results.append({
                'prompt_id': prompt_id,
                'task_id': result.id,
                'status': 'processing'
            })
        
        # Update task status
        current_task.update_state(
            state='SUCCESS',
            meta={
                'status': 'Batch optimization completed',
                'results': results
            }
        )
        
        return results
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Batch optimization failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def analyze_prompt_quality_task(self, prompt_id: int, user_id: int):
    """
    Background task for prompt quality analysis
    """
    try:
        from app.services.quality_service import QualityService
        from app.models.prompt import Prompt
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Get prompt
            prompt = db.query(Prompt).filter(
                Prompt.id == prompt_id,
                Prompt.user_id == user_id
            ).first()
            
            if not prompt:
                raise ValueError("Prompt not found")
            
            # Analyze quality
            quality_service = QualityService()
            quality_scores = quality_service.assess_prompt_quality(prompt.original_prompt)
            
            # Update prompt with quality scores
            prompt.clarity_score = quality_scores.get('clarity', 0)
            prompt.specificity_score = quality_scores.get('specificity', 0)
            prompt.overall_quality_score = quality_scores.get('overall', 0)
            
            db.commit()
            
            return {
                'prompt_id': prompt_id,
                'quality_scores': quality_scores
            }
            
        finally:
            db.close()
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Quality analysis failed',
                'error': str(e)
            }
        )
        raise 