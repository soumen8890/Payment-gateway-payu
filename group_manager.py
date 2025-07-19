from pyrogram import Client
from datetime import datetime
from config import Config

async def add_to_premium_group(client, user_id, invite_link):
    try:
        # In a real implementation, you would use the invite link
        # For demo, we'll just show the concept
        
        # Check if user already in group
        # member = await client.get_chat_member(Config.PREMIUM_GROUP_ID, user_id)
        # if member.status in ["member", "administrator", "creator"]:
        #     return True
        
        # Send the invite link to user
        await client.send_message(
            user_id,
            f"Here's your one-time invite link to the premium group:\n{invite_link}"
        )
        
        return True
        
    except Exception as e:
        print(f"Error adding user to group: {e}")
        return False

async def remove_expired_users(client):
    try:
        # Get all users whose subscription has expired
        # expired_users = get_expired_users_from_db()
        
        for user_id in expired_users:
            try:
                await client.ban_chat_member(
                    chat_id=Config.PREMIUM_GROUP_ID,
                    user_id=user_id
                )
                
                # Notify user
                await client.send_message(
                    user_id,
                    "Your premium subscription has expired. "
                    "To continue access, please renew your subscription."
                )
                
                # Log removal
                await client.send_message(
                    Config.LOG_CHANNEL_ID,
                    f"Removed user {user_id} - subscription expired"
                )
                
                # Update DB
                # update_user_status(user_id, "expired")
                
            except Exception as e:
                print(f"Error removing user {user_id}: {e}")
                
        return True
        
    except Exception as e:
        print(f"Error in remove_expired_users: {e}")
        return False
