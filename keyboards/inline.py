from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_phone_kb():
    # Создаем кнопку, которая запрашивает контакт
    contact_btn = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[contact_btn]],
        resize_keyboard=True,
        one_time_keyboard=True # Клавиатура скроется после нажатия
    )
    return keyboard

def get_main_kb() -> InlineKeyboardMarkup:
    """
    Создает главное меню бота с кнопками.
    """
    buttons = [
        # Первый ряд кнопок
        [
            InlineKeyboardButton(text="💆‍♂️ Услуги", callback_data="services"),
            InlineKeyboardButton(text="💰 Прайс", callback_data="price")
        ],
        # Второй ряд (одна широкая кнопка)
        [
            InlineKeyboardButton(text="📅 Записаться", callback_data="book")
        ],
        # Третий ряд (ссылка на внешние ресурсы, например, карты)
        [
            InlineKeyboardButton(text="📍 Наш адрес", url="https://yandex.ru/maps/-/CPAOA65I")
        ]
    ]

    # Сборка клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_cancel_kb() -> InlineKeyboardMarkup:
    """
    Дополнительная кнопка отмены (если понадобится в будущем).
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])
    return keyboard

def get_services_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура с выбором конкретных услуг.
    """
    buttons = [
        [InlineKeyboardButton(text="✂️ Мужская стрижка", callback_data="order_haircut")],
        [InlineKeyboardButton(text="🧔 Оформление бороды", callback_data="order_beard")],
        [InlineKeyboardButton(text="🔥 Комплексный уход", callback_data="order_combo")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")] # Хороший тон — дать вернуться
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)