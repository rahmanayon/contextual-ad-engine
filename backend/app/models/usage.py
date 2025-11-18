"""
Usage tracking database model.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class UsageLog(Base):
    """Usage log model for tracking generations."""
    
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    input_url = Column(String, nullable=False)
    generation_count = Column(Integer, default=1)
    ai_model_used = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
