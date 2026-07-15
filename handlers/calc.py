import ast
import operator

from aiogram import Router, types
from aiogram.filters import Command

from services.currency_api import convert, get_rates

router = Router()

# Xavfsiz matematik amallar (eval() o'rniga — xavfsizlik uchun muhim!)
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def safe_eval(expression: str) -> float:
    """
    Matematik ifodani xavfsiz hisoblaydi.
    eval() ishlatilmaydi — faqat ruxsat etilgan amallar (+, -, *, /, %, **) qabul qilinadi.
    """
    node = ast.parse(expression, mode="eval").body
    return _eval_node(node)


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Faqat sonlar ruxsat etilgan")
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"'{op_type.__name__}' amaliga ruxsat yo'q")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"'{op_type.__name__}' amaliga ruxsat yo'q")
        return _ALLOWED_OPERATORS[op_type](_eval_node(node.operand))
    else:
        raise ValueError("Ruxsat etilmagan ifoda")


@router.message(Command("calc"))
async def calc_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "Misol: <code>/calc 100+50*2 USD UZS</code>",
            parse_mode="HTML",
        )
        return

    parts = args[1].rsplit(maxsplit=2)  # [expression, from_cur, to_cur]

    if len(parts) == 3:
        expression, from_cur, to_cur = parts
    elif len(parts) == 1:
        expression, from_cur, to_cur = parts[0], None, None
    else:
        await message.answer(
            "Format noto'g'ri. Misol:\n"
            "<code>/calc 100+50*2 USD UZS</code> (valyutaga o'girish bilan)\n"
            "<code>/calc 100+50*2</code> (faqat hisoblash)",
            parse_mode="HTML",
        )
        return

    try:
        result = safe_eval(expression.replace(" ", ""))
    except (ValueError, SyntaxError, ZeroDivisionError, TypeError) as e:
        await message.answer(f"❌ Hisoblashda xatolik: ifodani tekshiring.\n(<i>{e}</i>)", parse_mode="HTML")
        return

    if from_cur is None:
        await message.answer(f"🧮 Natija: <b>{result:,.4f}</b>", parse_mode="HTML")
        return

    rates = await get_rates()
    from_cur, to_cur = from_cur.upper(), to_cur.upper()

    if rates is None or from_cur not in rates or to_cur not in rates:
        await message.answer(
            f"🧮 Ifoda natijasi: <b>{result:,.4f}</b>\n"
            f"⚠️ Ammo valyuta topilmadi yoki kurslarni olib bo'lmadi.",
            parse_mode="HTML",
        )
        return

    converted = await convert(result, from_cur, to_cur)
    await message.answer(
        f"🧮 Ifoda natijasi: <b>{result:,.4f}</b>\n"
        f"💱 {result:,.2f} {from_cur} = <b>{converted:,.2f} {to_cur}</b>",
        parse_mode="HTML",
    )
