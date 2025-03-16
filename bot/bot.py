import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Токен не найден в .env!")

bot = telebot.TeleBot(TOKEN)
API_URL = 'http://localhost:8000/api/register/'


@bot.message_handler(commands=['start'])
def handle_start(message):
    data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username or None  # Обработка отсутствия username
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            bot.reply_to(message, "✅ Регистрация успешна!")
        elif response.status_code == 200:
            bot.reply_to(message, "ℹ️ Вы уже зарегистрированы!")
        else:
            error_msg = response.json().get('error', 'Неизвестная ошибка')
            bot.reply_to(message, f"❌ Ошибка: {error_msg}")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, "⚠️ Сервер недоступен!")


@bot.message_handler(commands=['myinfo'])
def handle_myinfo(message):
    user_id = message.from_user.id
    try:
        response = requests.get(f'{API_URL}?user_id={user_id}')
        if response.status_code == 200:
            user_data = response.json()
            text = f"🆔 ID: {user_data['user_id']}\n👤 Username: {user_data['username'] or 'не указан'}"
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, "⚠️ Вы не зарегистрированы!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, "⚠️ Сервер недоступен!")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()