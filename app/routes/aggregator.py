from flask import Blueprint, jsonify, request
from app.utils.fetcher  import fetch_all_concurrent
from app.utils.storage  import save_to_db, get_latest_from_db

aggregator_bp = Blueprint("aggregator", __name__)


@aggregator_bp.route("/aggregate", methods=["GET"])
def aggregate():
    """
    GET /api/aggregate?city=Chennai&country=in&currency=USD

    Fetches live data from Weather, News, and Currency APIs
    concurrently and returns a unified JSON response.
    Also saves successful results to MySQL.
    """
    city     = request.args.get("city",     "Chennai")
    country  = request.args.get("country",  "in")
    currency = request.args.get("currency", "USD")

    # Fetch all APIs in parallel using threads
    results = fetch_all_concurrent(city, country, currency)

    # Save to DB
    save_to_db(results)

    return jsonify({
        "status":  "success",
        "query":   {"city": city, "country": country, "currency": currency},
        "data":    results
    }), 200


@aggregator_bp.route("/history", methods=["GET"])
def history():
    """
    GET /api/history?source=weather

    Returns recent records saved in MySQL.
    Optional query param: source (weather | news | currency)
    """
    source  = request.args.get("source", None)
    records = get_latest_from_db(source)

    return jsonify({
        "status":  "success",
        "count":   len(records),
        "records": records
    }), 200


@aggregator_bp.route("/weather", methods=["GET"])
def weather_only():
    """GET /api/weather?city=Mumbai — fetch only weather"""
    from app.services.weather_service import fetch_weather
    city   = request.args.get("city", "Chennai")
    result = fetch_weather(city)
    return jsonify(result), 200


@aggregator_bp.route("/news", methods=["GET"])
def news_only():
    """GET /api/news?country=in&category=technology — fetch only news"""
    from app.services.news_service import fetch_news
    country  = request.args.get("country",  "in")
    category = request.args.get("category", "technology")
    result   = fetch_news(country, category)
    return jsonify(result), 200


@aggregator_bp.route("/currency", methods=["GET"])
def currency_only():
    """GET /api/currency?base=USD — fetch only exchange rates"""
    from app.services.currency_service import fetch_currency
    base   = request.args.get("base", "USD")
    result = fetch_currency(base)
    return jsonify(result), 200
