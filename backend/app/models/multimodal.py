from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class PromptType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    CODE = "code"
    MULTIMODAL = "multimodal"


class MultimodalPrompt(Base):
    __tablename__ = "multimodal_prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prompt type and content
    prompt_type = Column(Enum(PromptType), nullable=False)
    text_content = Column(Text)
    
    # File storage references
    image_urls = Column(JSON)  # Array of image URLs
    audio_urls = Column(JSON)  # Array of audio URLs
    code_snippets = Column(JSON)  # Array of code snippets with language
    
    # Metadata
    title = Column(String(255))
    description = Column(Text)
    tags = Column(JSON)  # Array of tags
    
    # Processing information
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processing_notes = Column(Text)
    
    # Token and cost information
    total_tokens = Column(Integer)
    estimated_cost = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="multimodal_prompts")
    
    def __repr__(self):
        return f"<MultimodalPrompt(id={self.id}, type='{self.prompt_type}', status='{self.processing_status}')>"
    
    @property
    def has_images(self):
        return bool(self.image_urls and len(self.image_urls) > 0)
    
    @property
    def has_audio(self):
        return bool(self.audio_urls and len(self.audio_urls) > 0)
    
    @property
    def has_code(self):
        return bool(self.code_snippets and len(self.code_snippets) > 0)
    
    @property
    def content_summary(self):
        """Generate a summary of the multimodal content"""
        summary = []
        if self.text_content:
            summary.append(f"Text: {len(self.text_content)} chars")
        if self.has_images:
            summary.append(f"Images: {len(self.image_urls)} files")
        if self.has_audio:
            summary.append(f"Audio: {len(self.audio_urls)} files")
        if self.has_code:
            summary.append(f"Code: {len(self.code_snippets)} snippets")
        
        return ", ".join(summary) if summary else "No content"
    
    def add_image(self, image_url: str):
        """Add an image URL to the prompt"""
        if not self.image_urls:
            self.image_urls = []
        self.image_urls.append(image_url)
    
    def add_audio(self, audio_url: str):
        """Add an audio URL to the prompt"""
        if not self.audio_urls:
            self.audio_urls = []
        self.audio_urls.append(audio_url)
    
    def add_code(self, code: str, language: str = "text"):
        """Add a code snippet to the prompt"""
        if not self.code_snippets:
            self.code_snippets = []
        self.code_snippets.append({
            "code": code,
            "language": language,
            "added_at": func.now().isoformat()
        }) 