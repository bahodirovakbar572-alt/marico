import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Deploy uchun sozlamalar (Render) ---
# Agar WEBHOOK_URL berilgan bo'lsa (production/Render), bot webhook rejimida ishlaydi.
# Berilmagan bo'lsa (local kompyuter), bot polling rejimida ishlaydi.
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # masalan: https://mening-botim.onrender.com
WEBHOOK_PATH = "/webhook"
PORT = int(os.getenv("PORT", 8080))  # Render bu o'zgaruvchini avtomatik beradi

# Kurslarni olish uchun API (bepul, key kerak emas)
CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"

# Kurslarni necha soniyaga keshlash (default 30 daqiqa)
CACHE_TTL_SECONDS = 1800

# Tez-tez ishlatiladigan valyutalar (inline keyboard uchun)
POPULAR_CURRENCIES = ["USD", "EUR", "RUB", "UZS", "GBP", "TRY", "CNY", "KZT"]

# --- Self-ping (Render bepul tarifda "uxlab qolmasligi" uchun) ---
# Render bu manzilni avtomatik beradi, qo'lda kiritish shart emas
SELF_PING_URL = os.getenv("RENDER_EXTERNAL_URL")
SELF_PING_INTERVAL = 300  # soniya (5 daqiqa)