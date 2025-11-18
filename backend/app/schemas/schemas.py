"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# Auth schemas
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    email: str
    name: Optional[str]
    is_pro: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Generation schemas
class AdVariation(BaseModel):
    """Schema for a single ad copy variation."""
    headline: str
    body: str
    cta: str
    strategy: str


class GenerateRequest(BaseModel):
    """Schema for ad generation request."""
    url: str = Field(..., description="Target landing page URL")
    product_name: str = Field(..., description="Product or service name")
    value_props: List[str] = Field(..., description="Key value propositions")
    brand_voice: str = Field(..., description="Brand voice/tone")


class GenerateResponse(BaseModel):
    """Schema for ad generation response."""
    variations: List[AdVariation]
    scraped_content: Optional[str] = None


# Usage schemas
class UsageStats(BaseModel):
    """Schema for usage statistics."""
    total_generations: int
    limit: int
    remaining: int
    is_pro: bool
