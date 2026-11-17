import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

class CampusEventScraper:    

    # Initialize the scraper with a college calendar URL
    def __init__(self, url):
        self.url = url
        self.db_path = "db/campusconnect.db"

    # Download the college calendar webpage
    def fetch_page(self):
        response = requests.get(
            self.url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "xml")

    # Extract events from the college RSS calendar
    def parse_events(self, soup):
        events = []

        for item in soup.find_all("item"):
            title = item.find("title")
            date = item.find("pubDate")
            description = item.find("description")

            event = {
                "title": title.get_text(strip=True) if title else "No title",
                "date": date.get_text(strip=True) if date else "",
                "location": "",
                "description": description.get_text(" ", strip=True) if description else ""
            }

            events.append(event)

        return events


    # Save scraped college events into SQLite
    def save_events(self, events):
        if not events:
            print("No events found. Existing events will be kept.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear previously scraped events
        cursor.execute("DELETE FROM external_events")

        # Insert each scraped event
        for event in events:
            cursor.execute("""
                INSERT INTO external_events
                (title, date, location, description)
                VALUES (?, ?, ?, ?)
            """, (
                event["title"],
                event["date"],
                event["location"],
                event["description"]
            ))

        conn.commit()
        conn.close()

        print(f"Successfully saved {len(events)} events!")

