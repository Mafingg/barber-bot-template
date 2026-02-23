import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from keyboards.inline import get_main_kb, get_phone_kb, get_services_kb
from database import db
from datetime import datetime

router = Router()

# 1. Обработка команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}! 👋\n\n"
        "Чтобы мы могли подтвердить вашу запись, пожалуйста, "
        "поделитесь вашим номером телефона, нажав кнопку ниже.",
        reply_markup=get_phone_kb()
    )


# Хендлер для получения контакта
@router.message(F.contact)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number
    db.update_phone(message.from_user.id, phone)

    # Теперь, когда телефон у нас, показываем основное меню
    await message.answer(
        "✅ Спасибо! Ваш номер сохранен. Теперь вы можете пользоваться всеми услугами.",
        reply_markup=get_main_kb()  # Твое основное Inline-меню
    )

# 2. Обработка кнопки "Услуги"
@router.callback_query(F.data == "services")
async def show_services(callback: types.CallbackQuery):
    await callback.message.answer(
        "✂️ Наши услуги:\n"
        "— Мужская стрижка\n"
        "— Оформление бороды\n"
        "— Комплексный уход"
    )
    await callback.answer()

# 3. Обработка кнопки "Прайс"
@router.callback_query(F.data == "price")
async def show_price(callback: types.CallbackQuery):
    await callback.message.answer(
        "💰 Стоимость:\n"
        "— Стрижка: 1500₽\n"
        "— Борода: 1000₽\n"
        "— Комбо: 2200₽"
    )
    await callback.answer()


# 4. Начало записи: ПРИСЫЛАЕМ НОВОЕ сообщение с выбором услуг
@router.callback_query(F.data == "book")
async def book_start(callback: types.CallbackQuery):
    # Мы не редактируем старое, а шлем новое
    await callback.message.answer(
        "<b>Выберите услугу для записи:</b>",
        reply_markup=get_services_kb(),
        parse_mode="HTML"
    )
    # Обязательно отвечаем на колбэк, чтобы убрать "часики" с кнопки
    await callback.answer()

# Хендлер для выбора конкретной услуги
@router.callback_query(F.data.startswith("order_"))
async def process_order(callback: types.CallbackQuery, bot: Bot):
    admin_id = os.getenv("NOTIFICATION_CHAT_ID")

    # 1. Определяем название услуги
    services = {
        "order_haircut": "Мужская стрижка",
        "order_beard": "Оформление бороды",
        "order_combo": "Комплексный уход"
    }
    service_name = services.get(callback.data, "Неизвестная услуга")

    # 2. Достаем телефон из БД
    users = db.get_all_users()
    user_data = next((u for u in users if u[1] == callback.from_user.id), None)
    phone = user_data[4] if user_data and user_data[4] else "Номер не указан"

    # 3. Сообщение АДМИНУ
    admin_text = (
        f"⚡️ <b>НОВЫЙ ЗАКАЗ!</b>\n\n"
        f"👤 Клиент: {callback.from_user.full_name}\n"
        f"📞 Телефон: <code>{phone}</code>\n"
        f"🛠 Услуга: {service_name}\n"
        f"🕒 Время: {datetime.now().strftime('%H:%M')}"
    )

    # 4. НОВОЕ СООБЩЕНИЕ клиенту с подтверждением
    await callback.message.answer(
        f"✅ <b>Заявка принята!</b>\n\n"
        f"Вы записаны на: <i>{service_name}</i>\n"
        f"Администратор свяжется с вами в ближайшее время.",
        parse_mode="HTML"
    )

    # 5. Отправка уведомления админу
    await bot.send_message(chat_id=admin_id, text=admin_text, parse_mode="HTML")
    await callback.answer()

# 5. Кнопка "Назад" в таком стиле теперь просто дублирует главное меню новым сообщением
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.answer(
        "Вы вернулись в главное меню. Выберите раздел:",
        reply_markup=get_main_kb()
    )
    await callback.answer()