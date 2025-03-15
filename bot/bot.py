import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
API_URL = 'http://localhost:8000/api/register/'

@bot.message_handler(commands=['start'])
def handle_start(message):
    data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        bot.reply_to(message, "Вы успешно зарегистрированы!")
    else:
        bot.reply_to(message, "Ошибка регистрации")

@bot.message_handler(commands=['myinfo'])
def handle_myinfo(message):
    user_id = message.from_user.id
    response = requests.get(f'{API_URL}?user_id={user_id}')
    if response.status_code == 200:
        user_data = response.json()
        bot.reply_to(message, f"Ваши данные:\nID: {user_data['user_id']}\nUsername: {user_data['username']}")
    else:
        bot.reply_to(message, "Вы не зарегистрированы")

if __name__ == '__main__':
    bot.polling()