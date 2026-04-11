import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv
import sys

load_dotenv()
TOKEN = os.getenv('bot_token')
bot = telebot.TeleBot(TOKEN)

sticker = ['AAMCAgADGQEAA1xpvoQXYV7sgfr-MM1I0ICH2DoMdQACpRAAArRFoEpqI1qAWc6jRwEAB20AAzoE',
           'CAACAgIAAxkBAANcab6EF2Fe7IH6_jDNSNCAh9g6DHUAAqUQAAK0RaBKaiNagFnOo0c6BA']

@bot.message_handler(content_types=['sticker'])
def text(message):
    #print(message.sticker)
    bot.send_message(message.chat.id, text= "Sticker save")
    sticker.append(message.sticker.file_id)

@bot.message_handler(commands=['random_sticker'])
def text_2(message):
    #bot.send_sticker(message.chat.id, sticker[random.randint(0, len(sticker) - 1)])
    random_st = random.choice(sticker)
    bot.send_sticker(message.chat.id, random_st)

@bot.message_handler(commands=['stop'])
def text_3(message):
    bot.send_message(message.chat.id, text= "Stop bot")
    bot.stop_polling()
    sys.exit()

bot.infinity_polling()


