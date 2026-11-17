
import requests
import sqlite3


# API client that retrieves public data and saves it to SQLite
class APIClient:

    def __init__(self):
        self.url = "https://jsonplaceholder.typicode.com/posts"
        self.db_path = "db/campusconnect.db"

    # Send a GET request and retrieve JSON data
    def fetch_data(self):
        response = requests.get(self.url, timeout=15)
        response.raise_for_status()
        return response.json()

    # Save API data into the database
    def save_data(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_data (
                id INTEGER PRIMARY KEY,
                title TEXT,
                body TEXT
            )
        """)

        cursor.execute("DELETE FROM api_data")

        for item in data:
            cursor.execute("""
                INSERT INTO api_data (id, title, description)
                VALUES (?, ?, ?)
            """, (
                item["id"],
                item["title"],
                item["body"]
            ))

        conn.commit()
        conn.close()

        print(f"Successfully saved {len(data)} API records!")
