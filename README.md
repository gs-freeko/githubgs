# Multi-Source Data Aggregator

A backend pipeline built with **Flask** and **Python** that fetches data from
multiple third-party REST APIs (Weather, News, Currency) concurrently using
multithreading, normalizes it, stores it in **MySQL**, and exposes a unified
REST API for consumption.

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Tech Stack](#tech-stack)
3. [How It Works](#how-it-works)
4. [Setup & Installation](#setup--installation)
5. [API Endpoints](#api-endpoints)
6. [Key Concepts Explained](#key-concepts-explained)
7. [Interview Q&A](#interview-qa)

---

## Project Structure

```
data_aggregator/
│
├── run.py                          # Entry point — starts Flask server
├── config.py                       # API keys, DB config, base URLs
├── requirements.txt                # Python dependencies
│
└── app/
    ├── __init__.py                 # App factory (create_app)
    │
    ├── routes/
    │   ├── aggregator.py           # All API endpoints
    │   └── health.py               # Health check endpoint
    │
    ├── services/
    │   ├── weather_service.py      # Calls OpenWeatherMap API
    │   ├── news_service.py         # Calls NewsAPI
    │   └── currency_service.py     # Calls ExchangeRatesAPI
    │
    ├── models/
    │   └── database.py             # MySQL connection & table setup
    │
    └── utils/
        ├── fetcher.py              # Multithreaded concurrent fetcher
        └── storage.py              # Save & retrieve data from MySQL
```

---

## Tech Stack

| Technology            | Purpose                                      |
|-----------------------|----------------------------------------------|
| Python 3.10+          | Core language                                |
| Flask                 | Web framework / REST API                     |
| Requests              | HTTP calls to third-party APIs               |
| threading             | Concurrent API fetching (built-in module)    |
| MySQL                 | Persistent storage of aggregated data        |
| mysql-connector-python| MySQL driver for Python                      |
| Git                   | Version control                              |
| Linux                 | Deployment environment                       |

---

## How It Works

```
User hits GET /api/aggregate
          │
          ▼
   fetcher.py (multithreading)
   ┌────────────────────────────────┐
   │  Thread 1 → weather_service   │
   │  Thread 2 → news_service      │  ← All 3 run at the SAME time
   │  Thread 3 → currency_service  │
   └────────────────────────────────┘
          │
          ▼
   Results normalized & combined
          │
          ▼
   Saved to MySQL (aggregated_data table)
          │
          ▼
   Unified JSON response returned to user
```

---

## Setup & Installation

### Step 1 — Clone the project
```bash
git clone https://github.com/yourusername/data-aggregator.git
cd data-aggregator
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get free API keys
| API             | Where to get                         | Free Tier         |
|-----------------|--------------------------------------|-------------------|
| OpenWeatherMap  | https://openweathermap.org/api       | 1000 calls/day    |
| NewsAPI         | https://newsapi.org                  | 100 calls/day     |
| ExchangeRates   | https://exchangeratesapi.io          | 250 calls/month   |

### Step 5 — Set API keys in config.py
```python
WEATHER_API_KEY  = "your_key_here"
NEWS_API_KEY     = "your_key_here"
CURRENCY_API_KEY = "your_key_here"
```

### Step 6 — Set up MySQL
```sql
CREATE DATABASE data_aggregator;
```
Update `DB_CONFIG` in `config.py` with your MySQL credentials.

### Step 7 — Initialize database table
```bash
python -c "from app.models.database import init_db; init_db()"
```

### Step 8 — Run the server
```bash
python run.py
```
Server starts at → `http://localhost:5000`

---

## API Endpoints

### 1. Aggregate All Sources
```
GET /api/aggregate?city=Chennai&country=in&currency=USD
```
Fetches weather + news + currency concurrently and returns combined JSON.

**Sample Response:**
```json
{
  "status": "success",
  "query": { "city": "Chennai", "country": "in", "currency": "USD" },
  "data": {
    "weather": {
      "source": "weather",
      "city": "Chennai",
      "temperature": 32.5,
      "humidity": 78,
      "condition": "partly cloudy",
      "status": "success"
    },
    "news": {
      "source": "news",
      "articles": [
        { "title": "...", "source": "The Hindu", "published_at": "..." }
      ],
      "status": "success"
    },
    "currency": {
      "source": "currency",
      "base": "USD",
      "rates": { "INR": 83.5, "EUR": 0.92, "GBP": 0.79 },
      "status": "success"
    }
  }
}
```

---

### 2. Weather Only
```
GET /api/weather?city=Mumbai
```

### 3. News Only
```
GET /api/news?country=in&category=technology
```

### 4. Currency Only
```
GET /api/currency?base=USD
```

### 5. History (from MySQL)
```
GET /api/history
GET /api/history?source=weather
```
Returns last 10–30 records stored in MySQL.

### 6. Health Check
```
GET /api/health
```
```json
{ "status": "ok", "message": "Server is running" }
```

---

## Key Concepts Explained

### Why Multithreading?
Each API call waits for a network response (I/O-bound). Without threading:
- Weather API → 1 second wait
- News API    → 1 second wait
- Currency    → 1 second wait
- **Total: ~3 seconds**

With multithreading (all 3 run simultaneously):
- **Total: ~1 second** (slowest single call)

### Why Normalize API Responses?
Each API returns data in its own format. We extract only what matters
(temperature, headlines, rates) into a consistent structure so the caller
always gets a predictable response regardless of source.

### Why MySQL?
Storing historical data lets us:
- Track trends over time
- Serve cached results if an API is down
- Build analytics on top (future scope)

### Error Handling
Every service wraps its API call in try/except and returns a structured
error dict instead of crashing. This means even if one API fails, the
other two still return data.

---

## Interview Q&A

**Q: Why Flask over FastAPI?**
A: Flask is lightweight and simple for REST APIs. FastAPI would be better for
async — but since we're using threads for concurrency here, Flask works well.

**Q: Why threads and not asyncio?**
A: Threading is simpler to understand and works well for I/O-bound tasks like
API calls. Asyncio would require rewriting all services as async functions.

**Q: What happens if one API fails?**
A: Each service has its own try/except. It returns `{"status": "error", "message": "..."}`.
The other two APIs still succeed. The response includes all results — success or error.

**Q: How did you structure the database schema?**
A: One table `aggregated_data` with columns: source, data_key, data_value (JSON
string), fetched_at. Simple and flexible — works for all 3 sources without
needing 3 separate tables.

**Q: How would you scale this?**
A: Use a task queue (Celery + Redis) for scheduled fetching, add caching
(Redis) to avoid redundant API calls, and use connection pooling for DB.
