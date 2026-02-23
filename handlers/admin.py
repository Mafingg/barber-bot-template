import os
import asyncio
from aiogram import Router, types, Bot
from aiogram.filters import Command
from database import db

router = Router()


# Функция-фильтр для проверки админа
async def check_admin(message: types.Message):
    admin_id = os.getenv("NOTIFICATION_CHAT_ID")
    if str(message.from_user.id) != str(admin_id):
        await message.answer("❌ У вас нет прав для этой команды.")
        return False
    return True


@router.message(Command("admin"))
async def admin_menu(message: types.Message):
    if not await check_admin(message): return
    count = db.get_users_count()
    await message.answer(
        f"🛠 Панель администратора\n\n"
        f"👥 Всего пользователей: {count}\n\n"
        f"📜 Команды:\n"
        f"/users — Список всех клиентов\n"
        f"/broadcast — Рассылка (напишите текст после команды)"
    )


@router.message(Command("users"))
async def list_users(message: types.Message):
    if not await check_admin(message): return

    users = db.get_all_users()

    if not users:
        await message.answer("📭 База данных пока пуста.")
        return

    text = "📋 <b>Список клиентов в базе:</b>\n\n"

    for user in users:
        # Извлекаем данные (проверь индексы, если менял таблицу!)
        # По умолчанию: 2 - username, 3 - full_name, 4 - phone
        full_name = user[3] if user[3] else "Без имени"
        username = f"@{user[2]}" if user[2] else "Скрыт"
        phone = user[4] if user[4] else "Номер не указан"

        # Используем HTML-теги <b> (жирный) и <code> (моноширинный для копирования)
        text += (
            f"👤 <b>{full_name}</b>\n"
            f"🔗 Логин: {username}\n"
            f"📞 Тел: <code>{phone}</code>\n"
            f"────────────────\n"
        )

    # Проверка на длину сообщения
    if len(text) > 4000:
        await message.answer(text[:4000] + "...")
    else:
        # Указываем parse_mode="HTML"
        await message.answer(text, parse_mode="HTML")


@router.message(Command("broadcast"))
async def broadcast_handler(message: types.Message, bot: Bot):
    if not await check_admin(message): return

    # Забираем текст после команды /broadcast
    broadcast_text = message.text.replace("/broadcast", "").strip()

    if not broadcast_text:
        await message.answer("⚠️ Напишите текст рассылки после команды.\nПример: /broadcast Привет всем!")
        return

    users = db.get_all_users()
    await message.answer(f"🚀 Начинаю рассылку для {len(users)} чел...")

    success = 0
    failed = 0

    for user in users:
        try:
            await bot.send_message(chat_id=user[1], text=broadcast_text)
            success += 1
            # Небольшая пауза, чтобы Telegram не забанил за спам
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Ошибка отправки пользователю {user[1]}: {e}")
            failed += 1

    await message.answer(
        f"📢 Рассылка завершена!\n\n"
        f"✅ Успешно: {success}\n"
        f"❌ Ошибки: {failed}"
    )