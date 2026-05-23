import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv
import sys

load_dotenv()
TOKEN = os.getenv('bot_token')
bot = telebot.TeleBot(TOKEN)

user_dict = {}
class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.gender = None
        self.sticker = None

@bot.message_handler(commands=['register'])
def step_one(message):
    if message.chat.id in user_dict:
        user = user_dict[message.chat.id]
        text = f"Name = {user.name}\nAge = {user.age}\nGender = {user.gender}\nSticker = {user.sticker}"
        bot.send_message(message.chat.id, text)
        bot.send_sticker(message.chat.id, getattr(user, 'sticker', ''))
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Use save user")
        msg = bot.reply_to(message, "Hello, what is your name?", reply_markup=markup)

    bot.register_next_step_handler(msg, name_step)

def name_step(message):
    chat_id = message.chat.id
    if message.text == "Use save user":
        name = message.from_user.first_name
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, f"Ok, {name}\nHow old are you?")
    else:
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, f"Ok, {name}\nHow old are you?")

    bot.register_next_step_handler(msg, age_step)
def age_step(message):
    chat_id = message.chat.id
    user = user_dict[message.chat.id]
    text = message.text
    if not text.isdigit():
        msg = bot.reply_to(message, "Please enter an age")
        return
    user.age = int(text)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Boy")
    markup.add("Girl")
    msg = bot.send_message(chat_id, "What is your gender?", reply_markup=markup)

    bot.register_next_step_handler(msg, gender_step)
def gender_step(message):
    chat_id = message.chat.id
    user = user_dict[message.chat.id]
    if message.text == "Boy" or message.text == "Girl":
        user.gender = message.text
        msg = bot.send_message(chat_id, "What is favourite sticker?")
    else:
        msg = bot.reply_to(message, "Please choice")

    bot.register_next_step_handler(msg, sticker_step)


bot.infinity_polling()
