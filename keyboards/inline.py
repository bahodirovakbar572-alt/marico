from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import POPULAR_CURRENCIES


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💱 Konvertatsiya", callback_data="menu_convert")
    builder.button(text="📊 Kurslar", callback_data="menu_rates")
    builder.button(text="🧮 Hisob-kitob", callback_data="menu_calc")
    builder.adjust(1)
    return builder.as_markup()


def currency_from_keyboard() -> InlineKeyboardMarkup:
    """'Qaysi valyutadan' tanlash uchun tugmalar."""
    builder = InlineKeyboardBuilder()
    for code in POPULAR_CURRENCIES:
        builder.button(text=code, callback_data=f"from_{code}")
    builder.adjust(4)
    return builder.as_markup()


def currency_to_keyboard(from_code: str) -> InlineKeyboardMarkup:
    """'Qaysi valyutaga' tanlash uchun tugmalar (from_code dan tashqari)."""
    builder = InlineKeyboardBuilder()
    for code in POPULAR_CURRENCIES:
        if code != from_code:
            builder.button(text=code, callback_data=f"to_{from_code}_{code}")
    builder.adjust(4)
    return builder.as_markup()
