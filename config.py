import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8080))
BOT_TOKEN = os.getenv("BOT_TOKEN")

CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"

CACHE_TTL_SECONDS = 1800

POPULAR_CURRENCIES = ["USD", "EUR", "RUB", "UZS", "GBP", "TRY", "CNY", "KZT"]
