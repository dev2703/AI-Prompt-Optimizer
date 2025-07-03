from typing import Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.analytics import Analytics
from app.models.optimization import Optimization
from app.schemas.analytics import AnalyticsResponse, AnalyticsSummary

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get analytics summary for the specified period
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get optimizations in the period
    optimizations = db.query(Optimization).filter(
        and_(
            Optimization.user_id == current_user.id,
            Optimization.created_at >= start_date
        )
    ).all()
    
    if not optimizations:
        return AnalyticsSummary(
            total_optimizations=0,
            total_tokens_saved=0,
            total_cost_savings=0.0,
            average_token_reduction=0.0,
            average_quality_score=0.0,
            model_usage={},
            optimization_type_usage={},
            daily_stats=[]
        )
    
    # Calculate summary statistics
    total_optimizations = len(optimizations)
    total_tokens_saved = sum(opt.token_reduction or 0 for opt in optimizations)
    total_cost_savings = sum(opt.cost_savings or 0 for opt in optimizations)
    average_token_reduction = sum(opt.token_reduction_percentage or 0 for opt in optimizations) / total_optimizations
    average_quality_score = sum(opt.quality_score or 0 for opt in optimizations) / total_optimizations
    
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
    
    # Daily statistics
    daily_stats = []
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=i)
        day_optimizations = [opt for opt in optimizations if opt.created_at.date() == date.date()]
        
        daily_stats.append({
            "date": date.date().isoformat(),
            "optimizations": len(day_optimizations),
            "tokens_saved": sum(opt.token_reduction or 0 for opt in day_optimizations),
            "cost_savings": sum(opt.cost_savings or 0 for opt in day_optimizations)
        })
    
    return AnalyticsSummary(
        total_optimizations=total_optimizations,
        total_tokens_saved=total_tokens_saved,
        total_cost_savings=total_cost_savings,
        average_token_reduction=average_token_reduction,
        average_quality_score=average_quality_score,
        model_usage=model_usage,
        optimization_type_usage=optimization_type_usage,
        daily_stats=daily_stats
    )


@router.get("/daily", response_model=List[AnalyticsResponse])
async def get_daily_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get daily analytics data
    """
    query = db.query(Analytics).filter(Analytics.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Analytics.date >= start_date.date())
    if end_date:
        query = query.filter(Analytics.date <= end_date.date())
    
    analytics = query.order_by(Analytics.date.desc()).all()
    return [AnalyticsResponse.from_orm(analytic) for analytic in analytics]


@router.get("/performance")
async def get_performance_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get performance metrics and trends
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get optimizations with performance data
    optimizations = db.query(Optimization).filter(
        and_(
            Optimization.user_id == current_user.id,
            Optimization.created_at >= start_date
        )
    ).all()
    
    if not optimizations:
        return {
            "success_rate": 0.0,
            "average_processing_time": 0.0,
            "quality_trend": [],
            "efficiency_trend": []
        }
    
    # Calculate success rate
    successful = sum(1 for opt in optimizations if opt.quality_score and opt.quality_score >= 7.0)
    success_rate = (successful / len(optimizations)) * 100
    
    # Average processing time
    processing_times = [opt.processing_time for opt in optimizations if opt.processing_time]
    average_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
    
    # Quality trend (last 7 days)
    quality_trend = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        day_optimizations = [opt for opt in optimizations if opt.created_at.date() == date.date()]
        if day_optimizations:
            avg_quality = sum(opt.quality_score or 0 for opt in day_optimizations) / len(day_optimizations)
            quality_trend.append({
                "date": date.date().isoformat(),
                "average_quality": round(avg_quality, 2)
            })
    
    # Efficiency trend (token reduction over time)
    efficiency_trend = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        day_optimizations = [opt for opt in optimizations if opt.created_at.date() == date.date()]
        if day_optimizations:
            avg_efficiency = sum(opt.token_reduction_percentage or 0 for opt in day_optimizations) / len(day_optimizations)
            efficiency_trend.append({
                "date": date.date().isoformat(),
                "average_efficiency": round(avg_efficiency, 2)
            })
    
    return {
        "success_rate": round(success_rate, 2),
        "average_processing_time": round(average_processing_time, 2),
        "quality_trend": quality_trend,
        "efficiency_trend": efficiency_trend
    }


@router.get("/roi")
async def get_roi_analysis(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get ROI analysis and cost savings
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    optimizations = db.query(Optimization).filter(
        and_(
            Optimization.user_id == current_user.id,
            Optimization.created_at >= start_date
        )
    ).all()
    
    if not optimizations:
        return {
            "total_cost_savings": 0.0,
            "average_cost_savings_per_optimization": 0.0,
            "roi_percentage": 0.0,
            "projected_annual_savings": 0.0
        }
    
    total_cost_savings = sum(opt.cost_savings or 0 for opt in optimizations)
    average_cost_savings = total_cost_savings / len(optimizations)
    
    # Calculate ROI (assuming some base cost for the service)
    # This is a simplified calculation
    service_cost_per_optimization = 0.01  # $0.01 per optimization
    total_service_cost = len(optimizations) * service_cost_per_optimization
    roi_percentage = ((total_cost_savings - total_service_cost) / total_service_cost) * 100 if total_service_cost > 0 else 0
    
    # Project annual savings
    days_in_period = (datetime.utcnow() - start_date).days
    optimizations_per_day = len(optimizations) / days_in_period
    projected_annual_savings = optimizations_per_day * 365 * average_cost_savings
    
    return {
        "total_cost_savings": round(total_cost_savings, 4),
        "average_cost_savings_per_optimization": round(average_cost_savings, 4),
        "roi_percentage": round(roi_percentage, 2),
        "projected_annual_savings": round(projected_annual_savings, 2)
    } 