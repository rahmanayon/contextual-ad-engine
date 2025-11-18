"""
Webhook endpoints for external services (Stripe).
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import stripe
import logging
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        
        # Update user to Pro
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.is_pro = True
            db.commit()
            logger.info(f"User {user.id} upgraded to Pro")
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        
        # Downgrade user from Pro
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.is_pro = False
            db.commit()
            logger.info(f"User {user.id} downgraded from Pro")
    
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        status = subscription["status"]
        
        # Update user Pro status based on subscription status
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.is_pro = status == "active"
            db.commit()
            logger.info(f"User {user.id} subscription status: {status}")
    
    return {"status": "success"}
