"""
Ad generation API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.usage import UsageLog
from app.schemas.schemas import GenerateRequest, GenerateResponse
from app.services.scraper import ScraperService
from app.services.ai_service import AIService

router = APIRouter()
scraper = ScraperService()
ai_service = AIService()


@router.post("/generate", response_model=GenerateResponse)
async def generate_ad_copy(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate ad copy variations based on URL and product info."""
    
    # Check usage limits
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    usage_count = db.query(func.count(UsageLog.id)).filter(
        UsageLog.user_id == current_user.id,
        extract('month', UsageLog.created_at) == current_month,
        extract('year', UsageLog.created_at) == current_year
    ).scalar()
    
    limit = settings.PRO_TIER_LIMIT if current_user.is_pro else settings.FREE_TIER_LIMIT
    
    if usage_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Monthly generation limit ({limit}) reached. Please upgrade to Pro."
        )
    
    # Scrape the URL
    scraped_content = await scraper.scrape_url(request.url)
    
    # Generate ad copy
    try:
        variations = await ai_service.generate_ad_copy(
            product_name=request.product_name,
            value_props=request.value_props,
            brand_voice=request.brand_voice,
            scraped_content=scraped_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ad copy: {str(e)}"
        )
    
    # Log usage
    usage_log = UsageLog(
        user_id=current_user.id,
        input_url=request.url,
        generation_count=len(variations),
        ai_model_used=settings.GEMINI_MODEL
    )
    db.add(usage_log)
    db.commit()
    
    return GenerateResponse(
        variations=variations,
        scraped_content=scraped_content[:500] if scraped_content else None
    )
