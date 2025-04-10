import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import threading
from flask import Flask

# 🔐 Вставь сюда свой токен
TOKEN = "7357522794:AAHqsKsbtForBWBF9bzve6FUx-AXggD5dDc"
print(f"TOKEN is: {TOKEN}")
bot = telebot.TeleBot(TOKEN)

# 📚 Список уроков (видео и табы)
lessons = [
    {"videos": ["https://youtu.be/2j0QJC_wtn0"]},
    {"videos": ["https://youtu.be/quIvJs0LRBw"]},
    {"videos": ["https://youtu.be/5BW5AZzN_2c"]},
    {"videos": ["https://youtu.be/XIliqWpaCgQ"]},
    {"videos": ["https://youtu.be/VOe51uANd20"]},
    {"videos": ["https://youtu.be/buwcquAota4"]},
    {"videos": ["https://youtu.be/VLvKlR3sq_I"]},
    {"videos": ["https://youtu.be/21DArHOzkdw", "https://youtu.be/FgEOgw66FPk"], "tab": "урок08 Smoke on the water.pdf"},
    {"videos": ["https://youtu.be/UMiCbfDzNp0"], "tab": "урок09 Миссия Невыполнима.pdf"},
    {"videos": ["https://youtu.be/6E_BwkAnxnA"], "tab": "урок10 Prayer In C.pdf"},
    {"videos": ["https://youtu.be/k8k1FWbN_po"], "tab": "урок11-Лесник.pdf"},
    {"videos": ["https://youtu.be/2hgxVfV0Yh4"], "tab": "урок12-Черный Бумер.pdf"},
    {"videos": ["https://youtu.be/5wbZNOA7sWY"], "tab": "урок13-Длительности.pdf"},
    {"videos": ["https://youtu.be/SxDDwJtw2O8"], "tab": "урок14-Кукла Колдуна.pdf"},
    {"videos": ["https://youtu.be/PIBGDBw_ZIQ"], "tab": "урок15-Конь - Любэ.pdf"},
]

# 💾 Храним, какой урок был у пользователя
user_progress = {}

app = Flask(__name__)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# 📍 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Учиться 🎸", callback_data="learn")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы начать обучение:", reply_markup=keyboard)

# 📌 Обработка кнопки "Учиться"
@bot.callback_query_handler(func=lambda call: call.data == "learn")
def handle_learn(call):
    user_id = call.from_user.id
    index = user_progress.get(user_id, 0)

    if index >= len(lessons):
        bot.send_message(call.message.chat.id, "Ты прошёл все уроки! Молодец! 🎉")
        return

    lesson = lessons[index]
    bot.answer_callback_query(call.id, text="Отправляю урок...")

    # Отправка видео (может быть одно или два)
    for video in lesson["videos"]:
        bot.send_message(call.message.chat.id, video)

    # Если есть таб — отправить файл
    if "tab" in lesson:
        tab_path = os.path.join("tabs", lesson["tab"])
        if os.path.exists(tab_path):
            with open(tab_path, 'rb') as f:
                bot.send_document(call.message.chat.id, f)
        else:
            bot.send_message(call.message.chat.id, f"Таб {lesson['tab']} не найден 😢")

    # Обновить прогресс
    user_progress[user_id] = index + 1


def run_bot():
    bot.infinity_polling()

# ▶ Запуск
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_bot).start()