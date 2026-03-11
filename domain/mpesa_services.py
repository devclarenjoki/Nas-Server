import base64
import random
import httpx
from datetime import datetime
from infrastructure.database import db
from config import Config

class MpesaService:
    
    @staticmethod
    def generate_random_digits():
        """Generates a random 9-digit number."""
        return random.randint(100000000, 999999999)

    @staticmethod
    def get_mpesa_password():
        """Generates Password and Timestamp."""
        # Format: YYYYMMDDHHMMSS
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Password = Base64(Shortcode + Passkey + Timestamp)
        data_to_encode = f"{Config.MPESA_LIVE_SHORTCODE}{Config.MPESA_LIVE_PASSKEY}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        
        return {"password": password, "timestamp": timestamp}

    @staticmethod
    async def get_mpesa_credentials():
        """Fetches Access Token from Safaricom."""
        credentials = f"{Config.MPESA_LIVE_CONSUMER_KEY}:{Config.MPESA_LIVE_CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                Config.MPESA_LIVE_OAUTH_URL,
                headers=headers
            )
            data = response.json()
            print(response)
            return data.get("access_token")

    @staticmethod
    async def initiate_stk_push(phone: str, amount: float, account_reference: str):
        """Initiates STK Push and saves request to DB."""
        
        # 1. Generate ID and Credentials
        stk_digits = MpesaService.generate_random_digits()
        stk_id = f"SMDT{stk_digits}"
        
        access_token = await MpesaService.get_mpesa_credentials()
        if not access_token:
            raise Exception("Failed to retrieve M-Pesa access token")
            
        pwd_data = MpesaService.get_mpesa_password()
        
        # 2. Prepare Payload
        payload = {
            "BusinessShortCode": Config.MPESA_LIVE_SHORTCODE,
            "Password": pwd_data["password"],
            "Timestamp": pwd_data["timestamp"],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": Config.MPESA_LIVE_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": Config.CALLBACK_URL,
            "AccountReference": account_reference,
            "TransactionDesc": account_reference
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 3. Save Initial Request to DB (Pending state)
        document = {
            "phone": phone,
            "amount": str(amount),
            "stkId": stk_id,
            "TimestampGen": pwd_data["timestamp"],
            "PasswordGen": pwd_data["password"],
            "ChrequestId": "PENDING",
            "responseCode": "PENDING",
            "resultCode": "PENDING",
            "resultDesc": "PENDING",
            "created_at": datetime.utcnow()
        }
        
        # Insert into 'stk_transactions' collection
        db.get_collection("stk_transactions").insert_one(document)
        
        # 4. Call Safaricom API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    Config.MPESA_LIVE_STKURL,
                    json=payload,
                    headers=headers
                )
                
                resp_data = response.json()

                print(resp_data)
                
                # 5. Update DB with CheckoutRequestID
                checkout_id = resp_data.get("CheckoutRequestID")
                resp_code = resp_data.get("ResponseCode")
                
                if checkout_id:
                    db.get_collection("stk_transactions").update_one(
                        {"stkId": stk_id},
                        {"$set": {
                            "ChrequestId": checkout_id,
                            "responseCode": resp_code
                        }}
                    )
                
                return {
                    "stkId": stk_id,
                    "CheckoutRequestID": checkout_id,
                    "ResponseCode": resp_code,
                    "ResponseDescription": resp_data.get("ResponseDescription")
                }
                
        except Exception as e:
            # Log error but maybe don't crash, or update DB with error
            print(f"STK Push Error: {e}")
            raise e