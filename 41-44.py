import telebot
from telebot import types
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
TOKEN = os.getenv('bot_token')
bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        time TEXT,
        data TEXT
        )
        """)
db.commit()

def del_data():
    cursor.execute("SELECT id FROM schedule")
    result = cursor.fetchall()

    cursor.executemany(
        "DELETE FROM schedule WHERE id = ?",
        result
    )
    db.commit()

def insert_data():
    db_list = []
    for db_list_item in db_list:
        cursor.execute("INSERT INTO schedule (day, time, data) VALUES (?,?,?)",
                       (
                       db_list_item[0],
                       db_list_item[1],
                       db_list_item[2],
                        )
                       )
        db.commit()
#del_data()
#insert_data()
@bot.message_handler(commands=['schedule'])
def start(message):
    text = "Чим можу тобі допомогти?"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Весь розклад")
    markup.add("Розклад на один день")
    markup.add("Редагувати розклад")

    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, select)

def select(message):
    match message.text:
        case "Весь розклад":
            show_schedule(message)
        case "Розклад на один день":
            show_schedule_one_day(message)
        case "Редагувати розклад":
            edit_schedule(message)
            bot.send_message(message.chat.id, "Ok, почнемо редагувати")
        case _:
            bot.send_message(message.chat.id, "Такого вибору немає")
            start(message)
def show_schedule(message):
    cursor.execute("SELECT * FROM schedule")
    data = cursor.fetchall()

    if len(data) == 0:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Так")
        markup.add("Ні")
        text = "У мене немає даних, хочеш додати?"
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, select)
        return
#Умови так/ні
    week_day = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
    text = ""
    for day in week_day:
        cursor.execute("SELECT * FROM schedule WHERE day = ?", (day,))
        data = cursor.fetchall()
        text += f"\n📅 {day}\n"
        if len(data) == 0:
            text += "Немає даних\n"
        else:
            for x, y in enumerate(data):
                text += (
                    f"{x + 1}. "
                    f"ID: {y[0]} | "
                    f"🕒 {y[2]} | "
                    f"📚 {y[3]}\n"
                )

        text += "\n"
    bot.send_message(message.chat.id, text)

def show_schedule_one_day(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    week_day = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
    for day in week_day:
        markup.add(day)
    msg = bot.send_message(message.chat.id, "Обери день: ", reply_markup=markup)
    bot.register_next_step_handler(msg, show_day_result)

def show_day_result(message):
    cursor.execute("SELECT * FROM schedule WHERE day = ?", (message.text,))
    data = cursor.fetchall()
    text = f"\n📅 {message.text}\n\n"
    if len(data) == 0:
        text += "Немає даних\n"
    else:
        for x, y in enumerate(data):
            text += (
                f"{x + 1}. "
                f"ID: {y[0]} | "
                f"🕒 {y[2]} | "
                f"📚 {y[3]}\n"
            )
    bot.send_message(message.chat.id, text)

def edit_schedule(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Додати запис")
    markup.add("Видалити запис")
    markup.add("Видалити все")
    msg = bot.send_message(message.chat.id, "Що ти хочеш вибрати", reply_markup=markup)



    bot.register_next_step_handler(msg, edit_select)

def edit_select(message):
    match message.text:
        case "Додати запис":
            bot.send_message(message.chat.id, "Введи день:\nчас:\nпредмет:\nНаприклад:\nПонеділок 12:30 англійська")
            bot.register_next_step_handler(message, add_day)
        case "Видалити запис":
            bot.send_message(message.chat.id, "Введи id запису, який потрібно видалити")
            bot.register_next_step_handler(message, delete_day)
        case "Видалити все":
            cursor.execute("DELETE FROM schedule")
            db.commit()
            bot.send_message(message.chat.id, "Записи видалено")
        case _:
            bot.send_message(message.chat.id, "Помилка вибору")
    print(message.text)
def add_day(message):
    try:
        data = message.text.split()
        day = data[0]
        time = data[1]
        subject = " ".join(data[2:])
        cursor.execute("INSERT INTO schedule(day,time,data)VALUES(?,?,?)", (day, time, subject))
        db.commit()
        bot.send_message(message.chat.id, "Запис додано")
    except:
        bot.send_message(message.chat.id, "Помилка")

def delete_day(message):
    try:
        note_id = int(message.text)
        cursor.execute("DELETE FROM schedule WHERE id = ?", (note_id,))
        db.commit()
        bot.send_message(message.chat.id, "Запис видалено")
    except:
        bot.send_message(message.chat.id, "Помилка")


print("Бот працює...")
bot.infinity_polling()