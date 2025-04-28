

import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Load the model
model_name = "gpt2"  # You can choose a different model if needed
generator = pipeline('text-generation', model=model_name)

# Function to handle messages
def respond_to_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = generator(user_message, max_length=100, num_return_sequences=1)
    bot_response = response[0]['generated_text']
    update.message.reply_text(bot_response)

# Main function to start the bot
def main() -> None:
    updater = Updater("7695867957:AAEEvAgZ_OTJuaUn4aUhqRb8yxetaYRq4uY")  # Replace with your token
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond_to_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
