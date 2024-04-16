import telebot
from telebot import types
import google.generativeai as genai
import os

# Установка токена бота
token = ''  # Replace with your token
bot = telebot.TeleBot(token)

# Configure GeminiAI model
GEMINI_API_KEY = os.getenv('')  # Replace with your Gemini API key
genai.configure(api_key='')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Кнопка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кнопка 2")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    elif message.text == "Кнопка 2":
        bot.send_message(message.chat.id, 'Спасибо за прочтение статьи!')
    else:
        # Генерация ответа от GeminiAI
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message.text)
            bot.send_message(message.chat.id, response)
        except Exception as e:  # Specific exception handling
            if isinstance(e, ValueError):
                bot.send_message(message.chat.id, "Ошибка: Неверный формат ввода.")
            elif isinstance(e, ConnectionError):
                bot.send_message(message.chat.id, "Ошибка: Проблемы с подключением.")
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

bot.polling()
