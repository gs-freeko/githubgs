import os

# ─── API Keys ───────────────────────────────────────────────
# Replace these with your actual free API keys
# Weather  → https://openweathermap.org/api  (free tier)
# News     → https://newsapi.org             (free tier)
# Currency → https://exchangeratesapi.io     (free tier)

WEATHER_API_KEY = "69c2ef24fd2946c2de8adb3dd5d8ac2d"
NEWS_API_KEY    = "6e2bd89befbc461685374dbdbeab984e"
CURRENCY_API_KEY = "817d9d13cf1c8a40205023d9120d1058"

# ─── API Base URLs ───────────────────────────────────────────
WEATHER_URL  = "https://api.openweathermap.org/data/2.5/weather"
NEWS_URL     = "https://newsapi.org/v2/top-headlines"
CURRENCY_URL = "https://api.exchangeratesapi.io/v1/latest"

# ─── MySQL Database Config ───────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",              # ← empty string, XAMPP has no password
    "database": "data_aggregator",
}

# ─── App Config ──────────────────────────────────────────────
DEFAULT_CITY     = "Chennai"
DEFAULT_COUNTRY  = "in"
DEFAULT_CURRENCY = "USD"
