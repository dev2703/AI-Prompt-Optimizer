from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    
    # Template content
    name = Column(String(255), nullable=False)
    description = Column(Text)
    template_content = Column(Text, nullable=False)
    
    # Categorization
    category = Column(String(100), nullable=False)  # marketing, coding, writing, etc.
    industry = Column(String(100))  # tech, healthcare, finance, etc.
    tags = Column(JSON)  # Array of tags
    
    # Usage metrics
    usage_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Template properties
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    difficulty_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    
    # Token information
    estimated_tokens = Column(Integer)
    optimization_potential = Column(Float)  # Estimated reduction percentage
    
    # Metadata
    author = Column(String(255))
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Template(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    @property
    def average_rating_display(self):
        if self.rating_count > 0:
            return round(self.average_rating, 1)
        return 0.0
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
    
    def add_rating(self, rating: float):
        """Add a new rating and update average"""
        if 1 <= rating <= 5:
            total_rating = self.average_rating * self.rating_count + rating
            self.rating_count += 1
            self.average_rating = total_rating / self.rating_count 