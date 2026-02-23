import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Импортируем базу данных
from database import db

# Импортируем файлы с хендлерами
import handlers.common as common_file
import handlers.admin as admin_file  # Добавили админа



async def main():
    # 1. Загружаем переменные (токен и ID)
    load_dotenv()

    # 2. Создаем таблицу в БД (если её нет)
    db.create_table()

    # 3. Инициализируем бота и диспетчер
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # 4. ПОДКЛЮЧАЕМ РОУТЕРЫ (ПОРЯДОК ВАЖЕН!)
    # Сначала админ, потом все остальные
    dp.include_router(admin_file.router)
    dp.include_router(common_file.router)

    # Очистка очереди сообщений
    await bot.delete_webhook(drop_pending_updates=True)

    print("✅ Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)


# Исправленная проверка запуска
if __name__ == "__main__":
    asyncio.run(main())