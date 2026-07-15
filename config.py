import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Kurslarni olish uchun API (bepul, key kerak emas)
CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"

# Kurslarni necha soniyaga keshlash (default 30 daqiqa)
CACHE_TTL_SECONDS = 1800

# Tez-tez ishlatiladigan valyutalar (inline keyboard uchun)
POPULAR_CURRENCIES = ["USD", "EUR", "RUB", "UZS", "GBP", "TRY", "CNY", "KZT"]
