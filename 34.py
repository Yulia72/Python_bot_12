import telebot
from telebot import types
bot = telebot.TeleBot("8720479396:AAGAK5jkPDUHExUVpJjU9QKS6KVfKWkRbVw")

@bot.message_handler(commands=['lol'])
def text(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = types.KeyboardButton(text= "How are you?")
    button2 = types.KeyboardButton(text= "How are you today?")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "Choose something", reply_markup=keyboard)
    bot.register_next_step_handler(message, qwerty)
def qwerty(message):
    if message.text == "How are you?":
        bot.send_message(message.chat.id, "Not bad")
    elif message.text == "How are you today?":
        bot.send_message(message.chat.id, "Bad")
    else:
        bot.send_message(message.chat.id, "I don't understand you")

bot.polling()
