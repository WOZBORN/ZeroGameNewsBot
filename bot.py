import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import csv
from datetime import datetime
from parser import clean_old_entries, fetch_news  # Импорт функций из parser.py
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# CSV файл с новостями
csv_file = 'news.csv'
today_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение
    welcome_text = (
        "🎮 *Добро пожаловать!*\n\n"
        "Я бот для игровых новостей. 🌟\n"
        "Я могу показать тебе *свежие новости игровой индустрии*!\n\n"
        "Чтобы посмотреть сегодняшние новости, нажми кнопку ниже. ⬇️"
    )
    # Инлайн-кнопка для показа новостей
    markup = InlineKeyboardMarkup()
    news_button = InlineKeyboardButton("📰 Сегодняшние новости", callback_data='today_news')
    markup.add(news_button)
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)


# Обработка нажатия кнопки "Сегодняшние новости"
@bot.callback_query_handler(func=lambda call: call.data == 'today_news')
def send_today_news(call):
    # Отправляем сообщение о начале обновления новостей
    bot.answer_callback_query(call.id, "Обновляю новости... ⏳")
    clean_old_entries()  # Очистка устаревших новостей
    fetch_news()  # Обновление новостей

    # Считываем сегодняшние новости
    today_news = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['parsed_date'] == today_date:
                today_news.append(row)

    # Если новостей нет
    if not today_news:
        bot.send_message(call.message.chat.id, "😔 Сегодня новостей пока нет.")
        return

    # Отправляем новости по одной
    for news in today_news:
        img_url = news['img_url']
        title = news['title']
        post_url = news['post_url']

        # Создаем кнопку для открытия ссылки через WebApp
        markup = InlineKeyboardMarkup()
        webapp_button = InlineKeyboardButton(
            text="🔗 Открыть статью",
            web_app=WebAppInfo(url=post_url)
        )
        markup.add(webapp_button)

        # Если есть изображение, отправляем его
        if img_url:
            bot.send_photo(
                call.message.chat.id,
                img_url,
                caption=f"📰 *{title}*",
                parse_mode='Markdown',
                reply_markup=markup
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f"📰 *{title}*",
                parse_mode='Markdown',
                reply_markup=markup
            )

    bot.send_message(call.message.chat.id, "✅ Все новости за сегодня отправлены!")


# Запуск бота
bot.polling(none_stop=True)
