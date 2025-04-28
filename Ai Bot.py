import asyncio
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# =============== Configuration ===============
API_ID = '28146532'
API_HASH = 'a4df6e5587790397b77c703c68119feb'
BOT_TOKEN = '7695867957:AAEEvAgZ_OTJuaUn4aUhqRb8yxetaYRq4uY'

TARGET_GROUP_ID = -4631119909  # Your group ID

SUPPORT_USERNAME = "@Smartautomationsuppport_bot"  # Replace with your support username
OWNER_USERNAME = "@smartautomations"      # Replace with your owner username

# =============== Clients ===============
userbot = TelegramClient('userbot', API_ID, API_HASH)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Mapping between sent message ID and user ID
message_mapping = {}  # {userbot_message_id: user_id}

# =============== Functions ===============

# Handle /start command
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Ask Me any questions I will give you reply through chat gpt.\n\n"
        "Note:- This bot will make some mistakes so kindly check it again.\n\n"
        f"Face any issue contact us on :- {SUPPORT_USERNAME}\n\n"
        f"©️Bot was Owned by :- {OWNER_USERNAME}"
    )
    await update.message.reply_text(welcome_text)


def replace_text(response: str) -> str:
    response = response.replace("bisnu ray", "HANUMAN")
    response = response.replace("smart util", "Smart Automations")
    return response
    

# When a user sends a message to the bot (private chat)
async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        return

    user = update.effective_user
    text = update.message.text

    # Send initial thinking message to the group via userbot
    sent_message = await userbot.send_message(
        entity=TARGET_GROUP_ID,
        message=f"/ai {text}\n\nSmart AI is thinking..."  # Adding thinking message
    )

    # Map sent message ID to user ID
    message_mapping[sent_message.id] = user.id

    print(f"Mapped message {sent_message.id} to user {user.id}")

# When message is edited in group (edit handler)
@userbot.on(events.MessageEdited(chats=TARGET_GROUP_ID))
async def group_edit_handler(event):
    original_user_id = message_mapping.get(event.id)

    if original_user_id:
        # Wait for AI bot to edit the message with the final answer
        await asyncio.sleep(5)  # Give it some time to process and edit (adjust sleep time if necessary)

        # Refetch the latest version of the message (final answer)
        updated_message = await event.get_message()

        from telegram import Bot
        bot = Bot(token=BOT_TOKEN)

        await bot.send_message(
            chat_id=original_user_id,
            text=updated_message.text  # Send final AI answer to the user
        )
        print(f"Sent final edited reply to user {original_user_id}")

# =============== Main ===============
async def main():
    await userbot.start()
    print("Userbot Started")

    # Handlers for bot
    bot_app.add_handler(CommandHandler('start', start_handler))
    bot_app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, user_message_handler))
    
    bot_task = asyncio.create_task(bot_app.start())

    await userbot.run_until_disconnected()
    await bot_task

if __name__ == '__main__':
    asyncio.run(main())
  
