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

