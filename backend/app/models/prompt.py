from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class OptimizationType(str, enum.Enum):
    TOKEN_REDUCTION = "token_reduction"
    QUALITY_ENHANCEMENT = "quality_enhancement"
    CLARITY_IMPROVEMENT = "clarity_improvement"
    MULTIMODAL = "multimodal"
    MODEL_ADAPTATION = "model_adaptation"


class PromptStatus(str, enum.Enum):
    DRAFT = "draft"
    OPTIMIZING = "optimizing"
    COMPLETED = "completed"
    FAILED = "failed"


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prompt content
    original_prompt = Column(Text, nullable=False)
    optimized_prompt = Column(Text)
    prompt_type = Column(String(50), default="text")  # text, code, image, audio
    
    # Metadata
    title = Column(String(255))
    description = Column(Text)
    tags = Column(JSON)  # Array of tags
    category = Column(String(100))
    
    # Token information
    original_tokens = Column(Integer)
    optimized_tokens = Column(Integer)
    token_reduction_percentage = Column(Float)
    
    # Quality metrics
    clarity_score = Column(Float)  # 1-10 scale
    specificity_score = Column(Float)  # 1-10 scale
    overall_quality_score = Column(Float)  # 1-10 scale
    
    # Status and timestamps
    status = Column(Enum(PromptStatus), default=PromptStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="prompts")
    optimizations = relationship("Optimization", back_populates="prompt")
    
    def __repr__(self):
        return f"<Prompt(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def token_savings(self):
        if self.original_tokens and self.optimized_tokens:
            return self.original_tokens - self.optimized_tokens
        return 0
    
    @property
    def cost_savings(self):
        # This would be calculated based on model pricing
        return 0.0


class Optimization(Base):
    __tablename__ = "optimizations"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Optimization details
    optimization_type = Column(Enum(OptimizationType), nullable=False)
    model_used = Column(String(100))  # gpt-4, claude-3, etc.
    target_model = Column(String(100))  # For model adaptation
    
    # Results
    original_prompt = Column(Text, nullable=False)
    optimized_prompt = Column(Text, nullable=False)
    
    # Token analysis
    original_tokens = Column(Integer, nullable=False)
    optimized_tokens = Column(Integer, nullable=False)
    token_reduction = Column(Integer)  # Tokens saved
    token_reduction_percentage = Column(Float)
    
    # Quality metrics
    quality_score = Column(Float)  # 1-10 scale
    clarity_score = Column(Float)  # 1-10 scale
    specificity_score = Column(Float)  # 1-10 scale
    
    # Cost analysis
    original_cost = Column(Float)
    optimized_cost = Column(Float)
    cost_savings = Column(Float)
    cost_savings_percentage = Column(Float)
    
    # Optimization metadata
    optimization_notes = Column(Text)
    optimization_settings = Column(JSON)  # Settings used for optimization
    processing_time = Column(Float)  # Time taken in seconds
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prompt = relationship("Prompt", back_populates="optimizations")
    user = relationship("User", back_populates="optimizations")
    
    def __repr__(self):
        return f"<Optimization(id={self.id}, type='{self.optimization_type}', reduction='{self.token_reduction_percentage}%')>"
    
    def calculate_savings(self):
        """Calculate token and cost savings"""
        if self.original_tokens and self.optimized_tokens:
            self.token_reduction = self.original_tokens - self.optimized_tokens
            self.token_reduction_percentage = (self.token_reduction / self.original_tokens) * 100
        
        if self.original_cost and self.optimized_cost:
            self.cost_savings = self.original_cost - self.optimized_cost
            self.cost_savings_percentage = (self.cost_savings / self.original_cost) * 100 