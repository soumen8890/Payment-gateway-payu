import os

class Config:
    # Telegram API credentials
    API_ID = int(os.getenv("API_ID", 123456))
    API_HASH = os.getenv("API_HASH", "your_api_hash_here")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
    
    # MongoDB configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "premium_group_bot")
    
    # PayU Money credentials
    PAYU_MERCHANT_KEY = os.getenv("PAYU_MERCHANT_KEY", "your_merchant_key")
    PAYU_MERCHANT_SALT = os.getenv("PAYU_MERCHANT_SALT", "your_salt_key")
    PAYU_MODE = os.getenv("PAYU_MODE", "TEST")  # TEST or PROD
    
    # Telegram group and channel IDs
    PREMIUM_GROUP_ID = int(os.getenv("PREMIUM_GROUP_ID", -100123456789))
    LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", -100123456789))
    
    # Subscription plans (in INR)
    PLANS = {
        "weekly": 3,
        "monthly": 10,
        "yearly": 99
    }
    
    # Payment settings
    PAYMENT_SUCCESS_URL = "https://yourdomain.com/success"
    PAYMENT_FAILURE_URL = "https://yourdomain.com/failure"
    
    # Admin user IDs
    ADMIN_IDS = [123456789]  # Add your admin user IDs here
