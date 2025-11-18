"""
User profile and usage API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.usage import UsageLog
from app.schemas.schemas import UserResponse, UsageStats

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.get("/usage", response_model=UsageStats)
async def get_usage_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current month's usage statistics."""
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    total_generations = db.query(func.count(UsageLog.id)).filter(
        UsageLog.user_id == current_user.id,
        extract('month', UsageLog.created_at) == current_month,
        extract('year', UsageLog.created_at) == current_year
    ).scalar()
    
    limit = settings.PRO_TIER_LIMIT if current_user.is_pro else settings.FREE_TIER_LIMIT
    remaining = max(0, limit - total_generations)
    
    return UsageStats(
        total_generations=total_generations,
        limit=limit,
        remaining=remaining,
        is_pro=current_user.is_pro
    )
