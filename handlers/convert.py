from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.currency_api import convert, get_rate, get_rates
from keyboards.inline import currency_from_keyboard, currency_to_keyboard, main_menu_keyboard

router = Router()


class ConvertStates(StatesGroup):
    choosing_to = State()
    entering_amount = State()


# ---------- /convert 100 USD UZS  (to'g'ridan-to'g'ri buyruq) ----------
@router.message(Command("convert"))
async def convert_command(message: types.Message):
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.answer(
            "Noto'g'ri format. Misol:\n<code>/convert 100 USD UZS</code>",
            parse_mode="HTML",
        )
        return

    amount_str, from_cur, to_cur = args
    try:
        amount = float(amount_str)
    except ValueError:
        await message.answer("Miqdor son bo'lishi kerak. Masalan: 100")
        return

    await _send_conversion_result(message, amount, from_cur, to_cur)


# ---------- Oddiy matn: "100 USD UZS" ----------
@router.message(F.text.regexp(r"^\d+(\.\d+)?\s+[a-zA-Z]{3}\s+[a-zA-Z]{3}$"))
async def convert_plain_text(message: types.Message):
    amount_str, from_cur, to_cur = message.text.split()
    await _send_conversion_result(message, float(amount_str), from_cur, to_cur)


async def _send_conversion_result(message: types.Message, amount: float, from_cur: str, to_cur: str):
    rates = await get_rates()
    if rates is None:
        await message.answer("⚠️ Kurslarni olishda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.")
        return

    from_cur, to_cur = from_cur.upper(), to_cur.upper()
    if from_cur not in rates:
        await message.answer(f"❌ '{from_cur}' valyutasi topilmadi.")
        return
    if to_cur not in rates:
        await message.answer(f"❌ '{to_cur}' valyutasi topilmadi.")
        return

    result = await convert(amount, from_cur, to_cur)
    rate = await get_rate(from_cur, to_cur)

    await message.answer(
        f"💱 <b>{amount:,.2f} {from_cur}</b> = <b>{result:,.2f} {to_cur}</b>\n"
        f"📈 Kurs: 1 {from_cur} = {rate:,.4f} {to_cur}",
        parse_mode="HTML",
    )


# ---------- /rate USD UZS ----------
@router.message(Command("rate"))
async def rate_command(message: types.Message):
    args = message.text.split()[1:]
    if len(args) != 2:
        await message.answer("Misol: <code>/rate USD UZS</code>", parse_mode="HTML")
        return

    from_cur, to_cur = args[0].upper(), args[1].upper()
    rate = await get_rate(from_cur, to_cur)

    if rate is None:
        await message.answer("❌ Valyuta topilmadi yoki kurslarni olishda xatolik.")
        return

    await message.answer(f"📈 1 {from_cur} = {rate:,.4f} {to_cur}")


# ---------- Interaktiv rejim: tugmalar orqali ----------
@router.callback_query(F.data == "menu_rates")
async def menu_rates_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Qaysi valyutadan boshlaymiz?", reply_markup=currency_from_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("from_"))
async def choose_from_callback(callback: types.CallbackQuery, state: FSMContext):
    from_code = callback.data.split("_")[1]
    await state.update_data(from_code=from_code)
    await state.set_state(ConvertStates.choosing_to)
    await callback.message.edit_text(
        f"Tanlandi: {from_code}\n\nEndi qaysi valyutaga o'girmoqchisiz?",
        reply_markup=currency_to_keyboard(from_code),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("to_"), StateFilter(ConvertStates.choosing_to))
async def choose_to_callback(callback: types.CallbackQuery, state: FSMContext):
    _, from_code, to_code = callback.data.split("_")
    await state.update_data(to_code=to_code)
    await state.set_state(ConvertStates.entering_amount)
    await callback.message.edit_text(
        f"{from_code} ➜ {to_code}\n\nEndi miqdorni kiriting (masalan: 100):"
    )
    await callback.answer()


@router.message(StateFilter(ConvertStates.entering_amount))
async def enter_amount_handler(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Iltimos, faqat son kiriting. Masalan: 100")
        return

    data = await state.get_data()
    from_code, to_code = data["from_code"], data["to_code"]
    await state.clear()

    await _send_conversion_result(message, amount, from_code, to_code)
    await message.answer("Yana konvertatsiya qilish uchun /start bosing.", reply_markup=main_menu_keyboard())
