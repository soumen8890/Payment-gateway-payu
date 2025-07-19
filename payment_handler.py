import hashlib
import requests
from config import Config

async def generate_payment_link(user_id, amount, plan):
    try:
        # PayU Money payment link generation
        transaction_id = f"TXN{user_id}{int(time.time())}"
        product_info = f"Premium {plan} subscription"
        
        # Calculate hash
        hash_string = f"{Config.PAYU_MERCHANT_KEY}|{transaction_id}|{amount}|{product_info}|{user_id}|{Config.PAYU_MERCHANT_SALT}"
        hash_value = hashlib.sha512(hash_string.encode()).hexdigest().lower()
        
        # Payment data
        payment_data = {
            'key': Config.PAYU_MERCHANT_KEY,
            'txnid': transaction_id,
            'amount': amount,
            'productinfo': product_info,
            'firstname': "User",  # Will be updated with actual user name
            'email': "user@example.com",  # Will be updated with actual user email
            'phone': "9999999999",  # Will be updated with actual user phone
            'surl': Config.PAYMENT_SUCCESS_URL,
            'furl': Config.PAYMENT_FAILURE_URL,
            'hash': hash_value,
            'service_provider': 'payu_paisa',
            'udf1': user_id,
            'udf2': plan
        }
        
        # Store transaction details in DB
        # save_transaction(user_id, transaction_id, amount, plan, "pending")
        
        if Config.PAYU_MODE == "TEST":
            return "https://test.payu.in/_payment"
        else:
            return "https://secure.payu.in/_payment"
            
    except Exception as e:
        print(f"Error generating payment link: {e}")
        return None

async def verify_payment(utr):
    try:
        # Verify payment with PayU API
        # This is a simplified version - actual implementation depends on PayU's API
        
        # In a real implementation, you would call PayU's verification API
        # For demo purposes, we'll simulate a successful verification
        
        # Mock response - replace with actual API call
        mock_response = {
            "status": "success",
            "amount": 10.00,
            "productinfo": "Premium monthly subscription",
            "udf1": "123456789",  # user_id
            "udf2": "monthly"     # plan
        }
        
        if mock_response["status"] == "success":
            return {
                "success": True,
                "amount": mock_response["amount"],
                "user_id": mock_response["udf1"],
                "plan": mock_response["udf2"]
            }
        else:
            return {"success": False}
            
    except Exception as e:
        print(f"Payment verification error: {e}")
        return {"success": False}
