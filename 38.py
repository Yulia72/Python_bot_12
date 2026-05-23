import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv
import sys

load_dotenv()
TOKEN = os.getenv('bot_token')
bot = telebot.TeleBot(TOKEN)

MEMORY_DIR = 'bot_memory'
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

def gen_list():
    lists = []
    for _ in range(5):
        row = [str(random.randint(-50, 50)) for _ in range(10)]
        lists.append("\t".join(row))
    return "\n".join(lists)

def write_file(file_path, content):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(content)

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

@bot.message_handler(commands=['generate_document'])
def gen_new_file(message):
    bot.send_message(message.chat.id, "Яка назва файлу?")
    bot.register_next_step_handler(message, gen_send)

def gen_send(message):
    file_name = message.text
    file_path = os.path.join(MEMORY_DIR, file_name)
    random_date = gen_list()
    write_file(file_path, random_date)
    bot.send_message(message.chat.id, "Файл згенеровано")
    with open(file_path, "rb") as doc_to_send:
        bot.send_document(message.chat.id, doc_to_send)

@bot.message_handler(commands=['get_document'])
def request_file(message):
    bot.send_message(message.chat.id, "Який файл тобі потрібен?")
    bot.register_next_step_handler(message, check_file)

def check_file(message):
    file_name = message.text
    file_path = os.path.join(MEMORY_DIR, file_name)

bot.infinity_polling()




