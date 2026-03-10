from datetime import datetime
import pytz
from bson import ObjectId

class Order:
    def __init__(self, user_id, order_type, region,fiat_amount, fiat_currency, wallet_address, status="pending", fee=0.0, reference_id=None, created_at=None,expires_at=None, _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.type = order_type  # e.g., 'buy', 'sell'
        self.region = region

        self.fiat_amount = fiat_amount
        self.fiat_currency = fiat_currency
        self.wallet_address = wallet_address

        self.status = status
        self.fee = fee
        self.reference_id = self._generate_reference_id()
        self.created_at = created_at or datetime.now(pytz.UTC)

    def _generate_reference_id(self):
        """Generates a unique reference ID for the order"""
        # Simple implementation for demo; usually more complex
        import uuid
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def to_dict(self):
        return {
            
            "type": self.type,
            "region": self.region,
            "fiat_amount": self.fiat_amount,
            "fiat_currency": self.fiat_currency,
            "wallet_address": self.wallet_address,
            "status": self.status,
            "fee": self.fee,
            "reference_id": self.reference_id,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }