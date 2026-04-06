import requests
from config import CURRENCY_API_KEY, CURRENCY_URL

def fetch_currency(base: str = "USD") -> dict:
    """
    Fetch live exchange rates from ExchangeRatesAPI.

    Args:
        base (str): Base currency e.g. 'USD', 'EUR', 'INR'

    Returns:
        dict: Normalized exchange rates or error dict
    """
    try:
        params = {
            "access_key": CURRENCY_API_KEY,
            "base":       base,
            "symbols":    "INR,EUR,GBP,JPY,AUD"  # Only fetch relevant currencies
        }

        response = requests.get(CURRENCY_URL, params=params, timeout=5)
        response.raise_for_status()
        raw = response.json()

        if not raw.get("success", True):
            return {"source": "currency", "status": "error", "message": raw.get("error", {}).get("info", "Unknown error")}

        return {
            "source":    "currency",
            "base":      raw.get("base", base),
            "date":      raw.get("date", "N/A"),
            "rates":     raw.get("rates", {}),
            "status":    "success"
        }

    except requests.exceptions.Timeout:
        return {"source": "currency", "status": "error", "message": "Request timed out"}

    except requests.exceptions.HTTPError as e:
        return {"source": "currency", "status": "error", "message": str(e)}

    except Exception as e:
        return {"source": "currency", "status": "error", "message": str(e)}
