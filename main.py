import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

from config import BOT_TOKEN, PORT, SELF_PING_URL, SELF_PING_INTERVAL
from handlers.start import router as start_router
from handlers.convert import router as convert_router
from handlers.calc import router as calc_router

logging.basicConfig(level=logging.INFO)


async def self_ping_task():
    """
    Render bepul tarifida server 15 daqiqa harakatsizlikdan keyin uxlab qoladi.
    Shu funksiya har SELF_PING_INTERVAL soniyada botning o'zi o'ziga so'rov
    yuborib, uni doim "uyg'oq" holatda ushlab turadi.
    """
    if not SELF_PING_URL:
        logging.info("SELF_PING_URL topilmadi (local muhit) — self-ping o'chirilgan.")
        return

    await asyncio.sleep(30)  # server to'liq ishga tushguncha biroz kutamiz

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(SELF_PING_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    logging.info(f"Self-ping yuborildi: {resp.status}")
            except Exception as e:
                logging.warning(f"Self-ping xatolik: {e}")

            await asyncio.sleep(SELF_PING_INTERVAL)


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(convert_router)
    dp.include_router(calc_router)

    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="Bot ishlayapti"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    # Self-ping'ni fon vazifasi sifatida ishga tushiramiz
    asyncio.create_task(self_ping_task())

    logging.info("Bot ishga tushdi... Port: %s", PORT)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())