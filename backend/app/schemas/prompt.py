from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.prompt import PromptStatus, OptimizationType


class PromptBase(BaseModel):
    original_prompt: str = Field(..., min_length=1, max_length=10000)
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=100)
    prompt_type: str = Field(default="text", max_length=50)


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    original_prompt: Optional[str] = Field(None, min_length=1, max_length=10000)
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[PromptStatus] = None


class PromptResponse(PromptBase):
    id: int
    user_id: int
    optimized_prompt: Optional[str] = None
    original_tokens: Optional[int] = None
    optimized_tokens: Optional[int] = None
    token_reduction_percentage: Optional[float] = None
    clarity_score: Optional[float] = None
    specificity_score: Optional[float] = None
    overall_quality_score: Optional[float] = None
    status: PromptStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PromptList(BaseModel):
    prompts: List[PromptResponse]
    total: int
    page: int
    limit: int


class OptimizationRequest(BaseModel):
    prompt_id: Optional[int] = None
    original_prompt: str = Field(..., min_length=1, max_length=10000)
    optimization_type: OptimizationType = OptimizationType.TOKEN_REDUCTION
    target_model: Optional[str] = None
    reduction_target: Optional[float] = Field(None, ge=0.1, le=0.9)  # 10% to 90% reduction
    quality_threshold: Optional[float] = Field(None, ge=1.0, le=10.0)  # 1-10 scale


class OptimizationResponse(BaseModel):
    id: int
    prompt_id: int
    optimization_type: OptimizationType
    model_used: str
    original_prompt: str
    optimized_prompt: str
    original_tokens: int
    optimized_tokens: int
    token_reduction: int
    token_reduction_percentage: float
    quality_score: Optional[float] = None
    clarity_score: Optional[float] = None
    specificity_score: Optional[float] = None
    original_cost: Optional[float] = None
    optimized_cost: Optional[float] = None
    cost_savings: Optional[float] = None
    cost_savings_percentage: Optional[float] = None
    processing_time: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True 