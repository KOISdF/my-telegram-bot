import telebot
from telebot import types
from dotenv import load_dotenv
import os
from pathlib import Path

# Загружаем .env из папки с этим файлом
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Проверка, что данные подтянулись
print("BOT_TOKEN:", os.environ.get("BOT_TOKEN"))
print("ADMIN_ID:", os.environ.get("ADMIN_ID"))
print("GROUP_ID:", os.environ.get("GROUP_ID"))

# Получаем данные из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
GROUP_ID = os.environ.get("GROUP_ID")

if not BOT_TOKEN or not ADMIN_ID or not GROUP_ID:
    raise ValueError("Ошибка: BOT_TOKEN, ADMIN_ID и GROUP_ID должны быть заданы в .env")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "Привет! Напиши /join, чтобы подать заявку на вход.")
    else:
        bot.send_message(message.chat.id, "Админ-режим включён.")

# Команда /join для запроса ссылки
@bot.message_handler(commands=["join"])
def join_request(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Ты админ, тебе ссылка не нужна.")
        return

    # Отправляем админу запрос с кнопками "Одобрить" и "Отклонить"
    markup = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{message.chat.id}")
    reject_btn = types.InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{message.chat.id}")
    markup.add(approve_btn, reject_btn)

    bot.send_message(ADMIN_ID, f"Пользователь <b>{message.from_user.first_name}</b> (ID: {message.chat.id}) хочет войти.", reply_markup=markup)
    bot.send_message(message.chat.id, "Заявка отправлена админу. Ожидай ответа.")

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if not call.data:
        return

    action, user_id_str = call.data.split("_", 1)
    user_id = int(user_id_str)

    if action == "approve":
        try:
            # Генерируем одноразовую ссылку (1 использование, 1 день)
            invite_link = bot.create_chat_invite_link(chat_id=GROUP_ID, member_limit=1, expire_date=None)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Войти", url=invite_link.invite_link))

            bot.send_message(user_id, "✅ Ваша заявка одобрена! Нажмите кнопку, чтобы войти в группу:", reply_markup=markup)
            bot.send_message(ADMIN_ID, f"Пользователь {user_id} получил ссылку: {invite_link.invite_link}")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"Ошибка при создании ссылки: {e}")

    elif action == "reject":
        bot.send_message(user_id, "❌ Ваша заявка отклонена.")
        bot.send_message(ADMIN_ID, f"Пользователь {user_id} был отклонён.")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()

