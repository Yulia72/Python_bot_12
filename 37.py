import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv
import sys

load_dotenv()
TOKEN = os.getenv('bot_token')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def document(message):
    file = bot.get_file(message.document.file_id)
    down = bot.download_file(file.file_path)

    file_name = message.document.file_name
    with open(message.document.file_name, "wb") as f:
        f.write(down)
        bot.send_message(message.chat.id, f'File saved as: {file_name}')
    with open(file_name, "rb") as f:
        bot.send_document(message.chat.id, f)

bot.infinity_polling()