import stripe
from fastapi import APIRouter, HTTPException
from typing import Dict
from ..config import settings

router = APIRouter()

# Configure Stripe for ZAR
stripe.api_key = settings.STRIPE_SECRET_KEY

class ZARPaymentProcessor:
    def __init__(self):
        self.currency = "zar"
        self.payment_methods = ["card", "eft", "mobile"]
    
    async def create_payment_intent(self, amount: float, user_id: str, package: str) -> Dict:
        """Create payment intent in ZAR"""
        try:
            # Convert to cents
            amount_cents = int(amount * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=self.currency,
                metadata={
                    "user_id": user_id,
                    "package": package,
                    "integration_check": "accept_a_payment"
                }
            )
            
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
                "amount_zar": amount,
                "status": "requires_payment_method"
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def handle_webhook(self, payload: bytes, sig_header: str) -> Dict:
        """Handle Stripe webhooks for payment confirmation"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                await self._handle_successful_payment(payment_intent)
                
            return {"status": "success"}
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail="Invalid signature")
    
    async def _handle_successful_payment(self, payment_intent: Dict):
        """Process successful payment"""
        user_id = payment_intent['metadata']['user_id']
        package = payment_intent['metadata']['package']
        amount_zar = payment_intent['amount'] / 100
        
        # Activate user subscription
        await self._activate_user_subscription(user_id, package)
        
        # Log revenue
        await self._log_revenue(user_id, amount_zar, package)

PAYMENT_PACKAGES = {
    "basic": {
        "price_zar": 299,
        "features": ["Resume Optimization", "50 Job Applications/Month", "Basic Support"]
    },
    "professional": {
        "price_zar": 799,
        "features": ["Full Resume Rewrite", "Unlimited Applications", "Priority Support", "Cover Letters"]
    },
    "premium": {
        "price_zar": 1499,
        "features": ["All Professional Features", "Dedicated Job Agent", "Interview Preparation", "Career Coaching"]
    }
}
