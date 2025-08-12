import logging
from flask import Flask
import threading
import bot  # твой bot.py

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = Flask(__name__)

@app.route('/')
def home():
    logging.info("Запрос к / пришёл — бот жив")
    return "Bot is running!"

def run_bot():
    try:
        logging.info("Запуск бота...")
        bot.bot.infinity_polling()
    except Exception as e:
        logging.exception("Ошибка в работе бота:")

if __name__ == '__main__':
    logging.info("Запуск Flask-сервера и бота...")
    t = threading.Thread(target=run_bot)
    t.start()
    try:
        app.run(host='0.0.0.0', port=10000)
    except Exception as e:
        logging.exception("Ошибка в работе сервера:")
