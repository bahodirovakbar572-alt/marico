import time
import aiohttp
from config import CURRENCY_API_URL, CACHE_TTL_SECONDS

# Oddiy in-memory kesh: {"rates": {...}, "timestamp": 12345}
_cache = {"rates": None, "timestamp": 0}


async def _fetch_rates() -> dict | None:
    """API'dan barcha kurslarni oladi (baza sifatida USD ishlatiladi)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CURRENCY_API_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("rates")
                return None
    except (aiohttp.ClientError, TimeoutError):
        return None


async def get_rates() -> dict | None:
    """Keshlangan kurslarni qaytaradi, agar eskirgan bo'lsa yangilaydi."""
    now = time.time()
    if _cache["rates"] is None or (now - _cache["timestamp"]) > CACHE_TTL_SECONDS:
        rates = await _fetch_rates()
        if rates:
            _cache["rates"] = rates
            _cache["timestamp"] = now
        elif _cache["rates"] is None:
            return None
    return _cache["rates"]


async def convert(amount: float, from_currency: str, to_currency: str) -> float | None:
    """
    Bir valyutadan ikkinchisiga o'girish.
    Barcha kurslar USD bazasida bo'lgani uchun avval USD'ga o'giramiz.
    """
    rates = await get_rates()
    if rates is None:
        return None

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in rates or to_currency not in rates:
        return None

    # amount ni USD'ga o'girish, keyin maqsad valyutaga
    amount_in_usd = amount / rates[from_currency]
    result = amount_in_usd * rates[to_currency]
    return result


async def get_rate(from_currency: str, to_currency: str) -> float | None:
    """1 birlik from_currency ning to_currency dagi qiymatini qaytaradi."""
    return await convert(1, from_currency, to_currency)


def is_valid_currency(rates: dict, code: str) -> bool:
    return code.upper() in rates
