from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart

from keyboards.inline import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    text = (
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Men valyuta konvertatsiyasi va hisob-kitob botiman.\n\n"
        "📌 Buyruqlar:\n"
        "• <code>/convert 100 USD UZS</code> — valyutani o'girish\n"
        "• <code>/rate USD UZS</code> — 1 dona valyuta kursini ko'rish\n"
        "• <code>/calc 100+50*2 USD UZS</code> — hisoblab, so'ng o'girish\n\n"
        "Yoki quyidagi tugmalardan foydalaning 👇"
    )
    await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode="HTML")


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await start_handler(message)


@router.callback_query(F.data == "menu_convert")
async def menu_convert_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "Konvertatsiya uchun quyidagi formatda yozing:\n"
        "<code>/convert 100 USD UZS</code>\n\n"
        "yoki oddiygina: <code>100 USD UZS</code>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu_calc")
async def menu_calc_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "Hisob-kitob uchun quyidagi formatda yozing:\n"
        "<code>/calc 100+50*2 USD UZS</code>\n\n"
        "Bu 100+50*2 ni hisoblab, natijani USD dan UZS ga o'giradi.",
        parse_mode="HTML",
    )
    await callback.answer()
