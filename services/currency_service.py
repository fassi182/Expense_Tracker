import requests
from services.file_service import read_json, write_json
from logger_config import logger

CACHE_FILE = "data/rates_cache.json"

DEFAULT_RATES = {
    "usd": 278.50,
    "eur": 302.10,
    "gbp": 353.40,
    "inr": 3.35,
    "pkr": 1.0
}

CURRENCIES = ["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY","INR","SAR"]

# ---------------------- Get PKR Rate ----------------------
def get_pkr_rate(currency: str):
    """
    Returns the PKR conversion rate for a given currency.
    Fetches from API if online, else uses cache.
    """
    currency = currency.lower()
    if currency == "pkr":
        logger.info("PKR selected, rate = 1.0")
        return 1.0

    try:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency}.json"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        rate = res.json()[currency]["pkr"]
        logger.info(f"Fetched rate from API: 1 {currency.upper()} = {rate} PKR")

        # Update cache
        cache = read_json(CACHE_FILE, DEFAULT_RATES)
        cache[currency] = rate
        write_json(CACHE_FILE, cache)
        logger.info(f"Updated cache for {currency.upper()}")
        return rate

    except Exception as e:
        logger.warning(f"API fetch failed for {currency.upper()}, using cached rate: {e}")
        cached_rate = read_json(CACHE_FILE, DEFAULT_RATES).get(currency)
        if cached_rate:
            logger.info(f"Using cached rate: 1 {currency.upper()} = {cached_rate} PKR")
        else:
            logger.error(f"No cached rate available for {currency.upper()}")
        return cached_rate

# ---------------------- View All Rates ----------------------
def view_all_rates():
    logger.info("User selected: View All Exchange Rates")
    print("\n--- Current Exchange Rates (to PKR) ---")
    print("(Cached rates will be shown if offline)")
    print("-" * 35)
    
    for curr in CURRENCIES:
        rate = get_pkr_rate(curr)
        if rate:
            print(f"1 {curr:<5} = {rate:>8.2f} PKR")
        else:
            print(f"1 {curr:<5} = N/A")
    
    print("-" * 35)
    logger.info("Displayed all exchange rates to user")
