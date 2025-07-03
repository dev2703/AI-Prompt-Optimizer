from celery import current_task
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.analytics import Analytics
from app.models.optimization import Optimization


@celery_app.task(bind=True)
def update_daily_analytics_task(self, user_id: int, date: str = None):
    """
    Update daily analytics for a user
    """
    try:
        # Get database session
        db = SessionLocal()
        
        try:
            # Parse date
            if date:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            else:
                target_date = datetime.utcnow().date()
            
            # Get optimizations for the date
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            optimizations = db.query(Optimization).filter(
                and_(
                    Optimization.user_id == user_id,
                    Optimization.created_at >= start_datetime,
                    Optimization.created_at <= end_datetime
                )
            ).all()
            
            if not optimizations:
                # Create empty analytics record
                analytics = Analytics(
                    user_id=user_id,
                    date=target_date
                )
                db.add(analytics)
                db.commit()
                return {"status": "No optimizations found for date"}
            
            # Calculate metrics
            total_optimizations = len(optimizations)
            total_tokens_processed = sum(opt.original_tokens or 0 for opt in optimizations)
            total_tokens_saved = sum(opt.token_reduction or 0 for opt in optimizations)
            total_cost = sum(opt.original_cost or 0 for opt in optimizations)
            total_cost_savings = sum(opt.cost_savings or 0 for opt in optimizations)
            
            # Calculate averages
            processing_times = [opt.processing_time for opt in optimizations if opt.processing_time]
            avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
            
            quality_scores = [opt.quality_score for opt in optimizations if opt.quality_score]
            avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            # Model usage breakdown
            model_usage = {}
            for opt in optimizations:
                if opt.model_used:
                    model_usage[opt.model_used] = model_usage.get(opt.model_used, 0) + 1
            
            # Optimization type usage breakdown
            optimization_type_usage = {}
            for opt in optimizations:
                opt_type = str(opt.optimization_type)
                optimization_type_usage[opt_type] = optimization_type_usage.get(opt_type, 0) + 1
            
            # Success/failure counts
            successful_optimizations = sum(1 for opt in optimizations if opt.quality_score and opt.quality_score >= 7.0)
            failed_optimizations = total_optimizations - successful_optimizations
            
            # Create or update analytics record
            analytics = db.query(Analytics).filter(
                and_(
                    Analytics.user_id == user_id,
                    Analytics.date == target_date
                )
            ).first()
            
            if analytics:
                # Update existing record
                analytics.total_optimizations = total_optimizations
                analytics.total_tokens_processed = total_tokens_processed
                analytics.total_tokens_saved = total_tokens_saved
                analytics.total_cost = total_cost
                analytics.total_cost_savings = total_cost_savings
                analytics.average_optimization_time = avg_processing_time
                analytics.average_token_reduction = (total_tokens_saved / total_tokens_processed * 100) if total_tokens_processed > 0 else 0
                analytics.average_quality_score = avg_quality_score
                analytics.model_usage = model_usage
                analytics.optimization_type_usage = optimization_type_usage
                analytics.successful_optimizations = successful_optimizations
                analytics.failed_optimizations = failed_optimizations
            else:
                # Create new record
                analytics = Analytics(
                    user_id=user_id,
                    date=target_date,
                    total_optimizations=total_optimizations,
                    total_tokens_processed=total_tokens_processed,
                    total_tokens_saved=total_tokens_saved,
                    total_cost=total_cost,
                    total_cost_savings=total_cost_savings,
                    average_optimization_time=avg_processing_time,
                    average_token_reduction=(total_tokens_saved / total_tokens_processed * 100) if total_tokens_processed > 0 else 0,
                    average_quality_score=avg_quality_score,
                    model_usage=model_usage,
                    optimization_type_usage=optimization_type_usage,
                    successful_optimizations=successful_optimizations,
                    failed_optimizations=failed_optimizations
                )
                db.add(analytics)
            
            db.commit()
            
            return {
                "status": "Analytics updated successfully",
                "date": target_date.isoformat(),
                "total_optimizations": total_optimizations,
                "total_tokens_saved": total_tokens_saved,
                "total_cost_savings": total_cost_savings
            }
            
        finally:
            db.close()
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Analytics update failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def generate_weekly_report_task(self, user_id: int):
    """
    Generate weekly analytics report
    """
    try:
        # Get database session
        db = SessionLocal()
        
        try:
            # Get date range for last week
            end_date = datetime.utcnow().date()
            start_date = end_date - timedelta(days=7)
            
            # Get analytics for the week
            analytics = db.query(Analytics).filter(
                and_(
                    Analytics.user_id == user_id,
                    Analytics.date >= start_date,
                    Analytics.date <= end_date
                )
            ).all()
            
            if not analytics:
                return {"status": "No analytics data found for the week"}
            
            # Aggregate weekly metrics
            weekly_metrics = {
                "total_optimizations": sum(a.total_optimizations for a in analytics),
                "total_tokens_saved": sum(a.total_tokens_saved for a in analytics),
                "total_cost_savings": sum(a.total_cost_savings for a in analytics),
                "average_quality_score": sum(a.average_quality_score for a in analytics) / len(analytics),
                "success_rate": sum(a.successful_optimizations for a in analytics) / sum(a.total_optimizations for a in analytics) * 100 if sum(a.total_optimizations for a in analytics) > 0 else 0
            }
            
            # Aggregate model usage
            model_usage = {}
            for a in analytics:
                if a.model_usage:
                    for model, count in a.model_usage.items():
                        model_usage[model] = model_usage.get(model, 0) + count
            
            weekly_metrics["model_usage"] = model_usage
            
            return {
                "status": "Weekly report generated successfully",
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "metrics": weekly_metrics
            }
            
        finally:
            db.close()
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Weekly report generation failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def cleanup_old_analytics_task(self, days_to_keep: int = 90):
    """
    Clean up old analytics data
    """
    try:
        # Get database session
        db = SessionLocal()
        
        try:
            # Calculate cutoff date
            cutoff_date = datetime.utcnow().date() - timedelta(days=days_to_keep)
            
            # Delete old analytics records
            deleted_count = db.query(Analytics).filter(
                Analytics.date < cutoff_date
            ).delete()
            
            db.commit()
            
            return {
                "status": "Cleanup completed successfully",
                "deleted_records": deleted_count,
                "cutoff_date": cutoff_date.isoformat()
            }
            
        finally:
            db.close()
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Analytics cleanup failed',
                'error': str(e)
            }
        )
        raise 