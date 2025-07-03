from datetime import datetime, date
from typing import Optional, Dict, List
from pydantic import BaseModel


class AnalyticsBase(BaseModel):
    date: date
    total_optimizations: int
    total_tokens_processed: int
    total_tokens_saved: int
    total_cost: float
    total_cost_savings: float
    average_optimization_time: float
    average_token_reduction: float
    average_quality_score: float
    model_usage: Optional[Dict[str, int]] = None
    optimization_type_usage: Optional[Dict[str, int]] = None
    successful_optimizations: int
    failed_optimizations: int
    user_satisfaction_score: float


class AnalyticsResponse(AnalyticsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DailyStat(BaseModel):
    date: str
    optimizations: int
    tokens_saved: int
    cost_savings: float


class AnalyticsSummary(BaseModel):
    total_optimizations: int
    total_tokens_saved: int
    total_cost_savings: float
    average_token_reduction: float
    average_quality_score: float
    model_usage: Dict[str, int]
    optimization_type_usage: Dict[str, int]
    daily_stats: List[DailyStat]


class PerformanceMetrics(BaseModel):
    success_rate: float
    average_processing_time: float
    quality_trend: List[Dict[str, float]]
    efficiency_trend: List[Dict[str, float]]


class ROIAnalysis(BaseModel):
    total_cost_savings: float
    average_cost_savings_per_optimization: float
    roi_percentage: float
    projected_annual_savings: float 