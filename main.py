import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.convert import router as convert_router
from handlers.calc import router as calc_router

logging.basicConfig(level=logging.INFO)


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(convert_router)
    dp.include_router(calc_router)

    logging.info("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
