import mysql.connector
from config import DB_CONFIG

def get_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """
    Create the aggregated_data table if it doesn't exist.
    Call this once when the app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aggregated_data (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            source       VARCHAR(50)   NOT NULL,   -- 'weather', 'news', 'currency'
            data_key     VARCHAR(100)  NOT NULL,   -- e.g. city name, headline, currency pair
            data_value   TEXT          NOT NULL,   -- JSON string of the fetched data
            fetched_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized successfully.")
