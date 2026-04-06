import threading
from app.services.weather_service  import fetch_weather
from app.services.news_service     import fetch_news
from app.services.currency_service import fetch_currency

def fetch_all_concurrent(city: str, country: str, base_currency: str) -> dict:
    """
    Fetch data from Weather, News, and Currency APIs concurrently
    using Python multithreading.

    Why multithreading?
    - Each API call is an I/O-bound operation (waiting for network response)
    - Running them sequentially wastes time (e.g. 3 x 1s = 3s total wait)
    - With threads, all 3 run in parallel → total wait ≈ slowest single call (~1s)

    Args:
        city          (str): City name for weather
        country       (str): Country code for news
        base_currency (str): Base currency for exchange rates

    Returns:
        dict: Combined results from all 3 sources
    """

    results = {}  # Shared dict to store thread results

    def get_weather():
        results["weather"] = fetch_weather(city)

    def get_news():
        results["news"] = fetch_news(country)

    def get_currency():
        results["currency"] = fetch_currency(base_currency)

    # ── Create threads ──────────────────────────────────────
    t1 = threading.Thread(target=get_weather)
    t2 = threading.Thread(target=get_news)
    t3 = threading.Thread(target=get_currency)

    # ── Start all threads simultaneously ────────────────────
    t1.start()
    t2.start()
    t3.start()

    # ── Wait for all threads to finish ──────────────────────
    t1.join()
    t2.join()
    t3.join()

    return results
