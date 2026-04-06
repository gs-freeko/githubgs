import json
from app.models.database import get_connection

def save_to_db(results: dict):
    """
    Save aggregated API results into MySQL database.

    Args:
        results (dict): The combined results from all API fetches
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for source, data in results.items():
            if data.get("status") == "success":
                # Determine the key (city, country, or currency base)
                key = (
                    data.get("city") or
                    data.get("country") or
                    data.get("base") or
                    source
                )
                cursor.execute(
                    """
                    INSERT INTO aggregated_data (source, data_key, data_value)
                    VALUES (%s, %s, %s)
                    """,
                    (source, key, json.dumps(data))
                )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"❌ DB save error: {e}")

    finally:
        cursor.close()
        conn.close()


def get_latest_from_db(source: str = None) -> list:
    """
    Retrieve the latest records from the DB.

    Args:
        source (str): Optional filter — 'weather', 'news', 'currency'

    Returns:
        list: List of records as dicts
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if source:
            cursor.execute(
                "SELECT * FROM aggregated_data WHERE source = %s ORDER BY fetched_at DESC LIMIT 10",
                (source,)
            )
        else:
            cursor.execute(
                "SELECT * FROM aggregated_data ORDER BY fetched_at DESC LIMIT 30"
            )
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()
