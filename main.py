import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Define the Hindustan OTP website API endpoint
HINDUSTAN_OTP_API_ENDPOINT = "http://Hindustanotp.com/api/request_otp"

# Define your Telegram bot token
TOKEN = "6702401870:AAFKGVabGys609kT8G6DuPzNSJeFWZsJSBY"

# Define the owner's user ID
OWNER_USER_ID = 1728431821

# Define your account API key
ACCOUNT_API_KEY = "eyy2u7s53mxu0g8hzjzr9f9u443mx5e3"

# Define a dictionary to store user-specific OTP limits
# Format: {user_id: otp_limit}
user_otp_limits = {}

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the OTP Bot! Send /getotp to receive a one-time password.')

# Define the getotp command handler
def get_otp(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # Check if user has an OTP limit set
    if user_id in user_otp_limits:
        otp_limit = user_otp_limits[user_id]
        headers = {"Authorization": f"Bearer {ACCOUNT_API_KEY}"}
        response = requests.get(f"{HINDUSTAN_OTP_API_ENDPOINT}?limit={otp_limit}", headers=headers)
    else:
        headers = {"Authorization": f"Bearer {ACCOUNT_API_KEY}"}
        response = requests.get(HINDUSTAN_OTP_API_ENDPOINT, headers=headers)
    
    if response.status_code == 200:
        otps = response.json().get("otps")
        update.message.reply_text(f'Your OTPs are: {", ".join(otps)}')
    else:
        update.message.reply_text('Failed to retrieve OTPs. Please try again later.')

# Define the setlimit command handler
def set_limit(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_USER_ID:
        update.message.reply_text("Only the owner can set limits.")
        return
    
    if len(context.args) != 2:
        update.message.reply_text('Usage: /setlimit <user_id> <limit>')
        return
    
    try:
        user_id = int(context.args[0])
        limit = int(context.args[1])
        user_otp_limits[user_id] = limit
        update.message.reply_text(f'Limit set successfully for user {user_id}.')
    except ValueError:
        update.message.reply_text('Invalid arguments. Please provide a valid user ID and limit.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getotp", get_otp))
    dispatcher.add_handler(CommandHandler("setlimit", set_limit))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if name == 'main':
    main()
