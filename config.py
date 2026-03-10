import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    MONGODB_URL = os.getenv("MONGODB_URL")
    DB_NAME = os.getenv("DB_NAME")
    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  # 5 minutes

    RATES_API= os.getenv("RATES_API_URL")

    TRON_PRO_API_KEY=os.getenv("TRON_PRO_API_KEY")

    # SYSTEM_PRIVATE_KEY = os.getenv("SYSTEM_WALLET_PRIVATE_KEY") 
    # SYSTEM_ADDRESS = os.getenv("SYSTEM_WALLET_ADDRESS")

    MPESA_LIVE_SHORTCODE = os.getenv("MPESA_LIVE_SHORTCODE")
    MPESA_LIVE_PASSKEY = os.getenv("MPESA_LIVE_PASSKEY")
    MPESA_LIVE_CONSUMER_KEY = os.getenv("MPESA_LIVE_CONSUMER_KEY")
    MPESA_LIVE_CONSUMER_SECRET = os.getenv("MPESA_LIVE_CONSUMER_SECRET")
    MPESA_LIVE_OAUTH_URL = os.getenv("MPESA_LIVE_OAUTH_URL", "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials")
    MPESA_LIVE_STKURL = os.getenv("MPESA_LIVE_STKURL", "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest")
    
    # Callback URL (Your public IP or domain)
    CALLBACK_URL = os.getenv("CALLBACK_URL")


    HOST= "127.0.0.1"
    PORT = 8467
    DEBUG="True"

