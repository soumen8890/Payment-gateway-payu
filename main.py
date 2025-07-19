import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from payment_handler import generate_payment_link, verify_payment
from group_manager import add_to_premium_group, remove_expired_users
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Client(
    "premium_group_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Start command handler
@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user
    welcome_msg = f"""
👋 Hello {user.first_name}!

Welcome to our Premium Group Access Bot. 

💰 Subscription Plans:
- Weekly: ₹{Config.PLANS['weekly']}
- Monthly: ₹{Config.PLANS['monthly']}
- Yearly: ₹{Config.PLANS['yearly']}

Choose a plan to get access to our premium content.
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Weekly ₹3", callback_data="plan_weekly")],
        [InlineKeyboardButton("Monthly ₹10", callback_data="plan_monthly")],
        [InlineKeyboardButton("Yearly ₹99", callback_data="plan_yearly")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ])
    
    await message.reply_text(welcome_msg, reply_markup=keyboard)

# Plan selection handler
@app.on_callback_query(filters.regex("^plan_"))
async def handle_plan_selection(client, callback_query):
    plan = callback_query.data.split("_")[1]
    amount = Config.PLANS[plan]
    
    payment_link = await generate_payment_link(
        user_id=callback_query.from_user.id,
        amount=amount,
        plan=plan
    )
    
    if payment_link:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Pay Now", url=payment_link)],
            [InlineKeyboardButton("Verify Payment", callback_data=f"verify_{callback_query.from_user.id}")]
        ])
        
        await callback_query.edit_message_text(
            f"Please complete your payment of ₹{amount} for {plan} plan.\n\n"
            "After payment, click 'Verify Payment' with your UTR number.",
            reply_markup=keyboard
        )
    else:
        await callback_query.edit_message_text("Failed to generate payment link. Please try again later.")

# Payment verification handler
@app.on_callback_query(filters.regex("^verify_"))
async def handle_verification(client, callback_query):
    user_id = int(callback_query.data.split("_")[1])
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This verification is not for you!", show_alert=True)
        return
    
    await callback_query.edit_message_text(
        "Please reply with your UTR number (Transaction Reference ID) "
        "that you received from your payment."
    )
    
    # Store that we're expecting a UTR from this user
    # (Implementation depends on your storage solution)

# UTR verification handler
@app.on_message(filters.private & filters.regex(r"^[A-Za-z0-9]+$"))
async def handle_utr(client, message):
    # Check if this user was asked for UTR
    utr = message.text.strip()
    
    # Verify payment with PayU
    verification_result = await verify_payment(utr)
    
    if verification_result["success"]:
        user_id = message.from_user.id
        plan = verification_result["plan"]
        
        # Calculate expiry date based on plan
        if plan == "weekly":
            expiry = datetime.datetime.now() + datetime.timedelta(weeks=1)
        elif plan == "monthly":
            expiry = datetime.datetime.now() + datetime.timedelta(days=30)
        else:  # yearly
            expiry = datetime.datetime.now() + datetime.timedelta(days=365)
        
        # Generate one-time join link
        invite_link = await app.create_chat_invite_link(
            chat_id=Config.PREMIUM_GROUP_ID,
            member_limit=1,
            expire_date=expiry
        )
        
        # Save user data to database (implementation depends on your DB)
        # save_user_data(user_id, plan, expiry, utr)
        
        # Send the invite link to user
        await message.reply_text(
            f"Payment verified successfully! 🎉\n\n"
            f"Your {plan} subscription is active until {expiry.strftime('%Y-%m-%d')}.\n\n"
            f"Click below to join the premium group (link valid for 24 hours):\n"
            f"{invite_link.invite_link}\n\n"
            "Note: This link can only be used once.",
            disable_web_page_preview=True
        )
        
        # Log to admin channel
        await app.send_message(
            Config.LOG_CHANNEL_ID,
            f"💰 New subscription\n\n"
            f"User: {message.from_user.mention}\n"
            f"Plan: {plan}\n"
            f"Amount: ₹{Config.PLANS[plan]}\n"
            f"Expiry: {expiry.strftime('%Y-%m-%d')}\n"
            f"UTR: {utr}"
        )
    else:
        await message.reply_text(
            "Payment verification failed. Please check your UTR number and try again.\n"
            "If the problem persists, contact support."
        )

# Admin commands
@app.on_message(filters.command("stats") & filters.user(Config.ADMIN_IDS))
async def stats(client, message):
    # Get stats from database
    # total_users, active_subs, revenue = get_stats_from_db()
    
    await message.reply_text(
        "📊 Bot Statistics\n\n"
        f"Total Users: {total_users}\n"
        f"Active Subscriptions: {active_subs}\n"
        f"Total Revenue: ₹{revenue}"
    )

# Scheduled job to remove expired users
async def remove_expired_users_job():
    while True:
        await remove_expired_users(app)
        await asyncio.sleep(3600)  # Check every hour

if __name__ == "__main__":
    # Start the bot
    app.run()
