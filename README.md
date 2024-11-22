# 🎮 Telegram Bot для новостей игровой индустрии

Этот бот создан для получения и отображения свежих новостей из мира игровой индустрии. Новости парсятся с сайта и отправляются пользователю в виде сообщений с возможностью открыть статью через Telegram WebApp.

---

## 📋 Функциональность
1. **Приветственное сообщение**:
   - При команде `/start` бот приветствует пользователя и предлагает посмотреть свежие новости игровой индустрии.
   
2. **Парсинг новостей**:
   - Бот использует скрипт для парсинга сайта с новостями.
   - Обновляет локальный файл `news.csv`, удаляя устаревшие данные и добавляя только сегодняшние новости.

3. **Отправка новостей**:
   - Новости отправляются пользователю с изображением, заголовком и кнопкой для открытия статьи через Telegram WebApp.

---

## 🛠️ Технологии
- **Python 3.10+**
- **Telebot**: библиотека для работы с Telegram API.
- **BeautifulSoup4**: парсинг HTML-кода новостного сайта.
- **Requests**: HTTP-запросы для получения данных с сайта.
- **Python-dotenv**: работа с переменными окружения.

---

## 🚀 Установка и запуск

### 1. Склонируйте репозиторий
```bash
git clone https://github.com/your-repo/telegram-news-bot.git
cd telegram-news-bot
```

### 2. Установите зависимости
Убедитесь, что у вас установлен Python версии 3.10 или выше. Затем установите необходимые зависимости:
```bash
pip install -r requirements.txt
```

### 3. Настройте файл `.env`
Создайте файл `.env` в корне проекта и добавьте в него токен вашего Telegram-бота:
```
TELEGRAM_TOKEN=ваш_токен
```

### 4. Запустите бота
```bash
python bot.py
```

---

## 📁 Структура проекта
```
telegram-news-bot/
│
├── bot.py             # Основной файл с логикой Telegram-бота
├── parser.py          # Скрипт для парсинга новостей
├── news.csv           # Файл с новостями (обновляется автоматически)
├── requirements.txt   # Список зависимостей
├── .env               # Переменные окружения (хранит токен)
└── README.md          # Документация проекта
```

---

## 🔧 Конфигурация

### Переменные окружения
- `TELEGRAM_TOKEN`: токен вашего Telegram-бота, полученный через [BotFather](https://t.me/BotFather).

---

## ⚙️ Основные команды
- **`/start`**: Приветствие и предложение посмотреть новости.
- Кнопка **"📰 Сегодняшние новости"**: Запускает обновление и отправку новостей.

---

## 📰 Как это работает

1. **Парсинг новостей**:
   - Используется файл `parser.py`, который парсит сайт, фильтруя только сегодняшние новости.
   - Данные сохраняются в `news.csv` в формате:
     ```
     data_key, title, img_url, post_url, parsed_date
     ```

2. **Отправка новостей**:
   - Каждая новость отправляется в виде сообщения с изображением, заголовком и кнопкой для открытия статьи через Telegram WebApp.

---

## 📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее читайте в [LICENSE](LICENSE).

---

## 💡 Идеи для доработки
- Добавить возможность выбора категории новостей.
- Реализовать поиск по новостям.
- Настроить регулярное обновление новостей по расписанию.

---

## 🙌 Благодарности
- [Telebot](https://github.com/eternnoir/pyTelegramBotAPI)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)