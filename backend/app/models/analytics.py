from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Date tracking
    date = Column(Date, nullable=False, default=func.current_date())
    
    # Usage metrics
    total_optimizations = Column(Integer, default=0)
    total_tokens_processed = Column(Integer, default=0)
    total_tokens_saved = Column(Integer, default=0)
    
    # Cost metrics
    total_cost = Column(Float, default=0.0)
    total_cost_savings = Column(Float, default=0.0)
    
    # Performance metrics
    average_optimization_time = Column(Float, default=0.0)
    average_token_reduction = Column(Float, default=0.0)
    average_quality_score = Column(Float, default=0.0)
    
    # Model usage breakdown
    model_usage = Column(JSON)  # {"gpt-4": 10, "claude-3": 5, ...}
    optimization_type_usage = Column(JSON)  # {"token_reduction": 8, "quality_enhancement": 7, ...}
    
    # Quality metrics
    successful_optimizations = Column(Integer, default=0)
    failed_optimizations = Column(Integer, default=0)
    user_satisfaction_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analytics")
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, user_id={self.user_id}, date='{self.date}')>"
    
    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        total = self.successful_optimizations + self.failed_optimizations
        if total > 0:
            return (self.successful_optimizations / total) * 100
        return 0.0
    
    @property
    def cost_savings_percentage(self):
        """Calculate cost savings percentage"""
        if self.total_cost > 0:
            return (self.total_cost_savings / self.total_cost) * 100
        return 0.0
    
    @property
    def token_savings_percentage(self):
        """Calculate token savings percentage"""
        if self.total_tokens_processed > 0:
            return (self.total_tokens_saved / self.total_tokens_processed) * 100
        return 0.0
    
    def update_metrics(self, optimization_data: dict):
        """Update analytics with new optimization data"""
        self.total_optimizations += 1
        self.total_tokens_processed += optimization_data.get('original_tokens', 0)
        self.total_tokens_saved += optimization_data.get('tokens_saved', 0)
        self.total_cost += optimization_data.get('cost', 0.0)
        self.total_cost_savings += optimization_data.get('cost_savings', 0.0)
        
        # Update averages
        if self.total_optimizations > 0:
            self.average_token_reduction = self.total_tokens_saved / self.total_tokens_processed * 100
            self.average_quality_score = (
                (self.average_quality_score * (self.total_optimizations - 1) + 
                 optimization_data.get('quality_score', 0)) / self.total_optimizations
            )
        
        # Update model usage
        model_used = optimization_data.get('model_used')
        if model_used:
            if not self.model_usage:
                self.model_usage = {}
            self.model_usage[model_used] = self.model_usage.get(model_used, 0) + 1
        
        # Update optimization type usage
        opt_type = optimization_data.get('optimization_type')
        if opt_type:
            if not self.optimization_type_usage:
                self.optimization_type_usage = {}
            self.optimization_type_usage[opt_type] = self.optimization_type_usage.get(opt_type, 0) + 1 