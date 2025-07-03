from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    
    # Usage limits
    monthly_optimizations = Column(Integer, default=50)  # Free tier limit
    optimizations_used = Column(Integer, default=0)
    monthly_tokens = Column(Integer, default=10000)  # Free tier limit
    tokens_used = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    prompts = relationship("Prompt", back_populates="user")
    optimizations = relationship("Optimization", back_populates="user")
    analytics = relationship("Analytics", back_populates="user")
    multimodal_prompts = relationship("MultimodalPrompt", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', tier='{self.subscription_tier}')>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def optimizations_remaining(self):
        return max(0, self.monthly_optimizations - self.optimizations_used)
    
    @property
    def tokens_remaining(self):
        return max(0, self.monthly_tokens - self.tokens_used)
    
    def can_optimize(self, estimated_tokens: int = 0) -> bool:
        """Check if user can perform optimization based on limits"""
        if not self.is_active:
            return False
        
        if self.subscription_tier == SubscriptionTier.ENTERPRISE:
            return True
        
        if self.optimizations_used >= self.monthly_optimizations:
            return False
        
        if self.tokens_used + estimated_tokens > self.monthly_tokens:
            return False
        
        return True
    
    def record_optimization(self, tokens_used: int):
        """Record optimization usage"""
        self.optimizations_used += 1
        self.tokens_used += tokens_used 