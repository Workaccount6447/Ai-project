# ========== Start a Dummy Web Server (for Health Checks) ==========
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

def run_web_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running successfully.")

    server = HTTPServer(('', 8000), SimpleHandler)
    logging.info("Starting health check server on port 8000...")
    server.serve_forever()

# Start webserver in a separate thread
threading.Thread(target=run_web_server, daemon=True).start()

# ========== Start Telegram Bot ==========
import asyncio
from telethon import TelegramClient, events
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# =============== Configuration ===============
API_ID = '28146532'  # Replace with your real API ID
API_HASH = 'a4df6e5587790397b77c703c68119feb'  # Replace with your real API Hash
BOT_TOKEN = '7695867957:AAEEvAgZ_OTJuaUn4aUhqRb8yxetaYRq4uY'  # Replace with your real bot token

TARGET_GROUP_ID = -4631119909  # Your group ID

SUPPORT_USERNAME = "@Smartautomationsuppport_bot"  # Support username
OWNER_USERNAME = "@smartautomations"               # Owner username

# =============== Clients ===============
userbot = TelegramClient('userbot', API_ID, API_HASH)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Mapping between sent message ID and user ID
message_mapping = {}  # {userbot_message_id: user_id}

# =============== Functions ===============

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Ask me any questions, I will reply through ChatGPT.\n\n"
        "Note: This bot may make mistakes, so kindly check the answers.\n\n"
        f"Facing any issue? Contact: {SUPPORT_USERNAME}\n\n"
        f"©️ Owned by: {OWNER_USERNAME}"
    )
    await update.message.reply_text(welcome_text)

def replace_text(response: str) -> str:
    response = response.replace("bisnu ray", "HANUMAN")
    response = response.replace("smart util", "Smart Automations")
    return response

async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        return

    user = update.effective_user
    text = update.message.text
    logging.info(f"Received message from {user.id}: {text}")

    sent_message = await userbot.send_message(
        entity=TARGET_GROUP_ID,
        message=f"/ai {text}\n\nSmart AI is thinking..."
    )

    message_mapping[sent_message.id] = user.id
    logging.info(f"Mapped message {sent_message.id} to user {user.id}")

@userbot.on(events.MessageEdited(chats=TARGET_GROUP_ID))
async def group_edit_handler(event):
    original_user_id = message_mapping.get(event.id)

    if original_user_id:
        await asyncio.sleep(5)

        updated_message = await event.get_message()

        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=original_user_id,
            text=updated_message.text
        )
        logging.info(f"Sent final edited reply to user {original_user_id}")

# =============== Main ===============

async def main():
    await userbot.start()
    logging.info("User   bot Started")

    await bot_app.initialize()
    await bot_app.start()

    # Register command handler
    bot_app.add_handler(CommandHandler("start", start_handler))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message_handler))

    try:
        await bot_app.updater.start_polling()
        await userbot.run_until_disconnected()
    finally:
        logging.info("Shutting down bot app...")
        await bot_app.updater.stop()
        await bot_app.stop()
        await bot_app.shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
