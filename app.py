from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from email.utils import parsedate_to_datetime
from routes.auth_routes import auth_bp
from routes.api_routes import api_bp
from routes.event_routes import event_bp
import os
import threading
import time
from utils.event_scraper import CampusEventScraper

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

# Define what they user should see when they visit the root URL

@app.route("/")
def index():
    conn = sqlite3.connect("db/campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    
    # Get automatically scraped events
    cursor.execute("SELECT * FROM external_events")
    automatic_events = cursor.fetchall()

    # Get manually added events
    cursor.execute("SELECT * FROM manual_events")
    manual_events = cursor.fetchall()

    # Combine both types of events
    events = automatic_events + manual_events


    # Format dates and show only upcoming events
    upcoming_events = []
    now = datetime.now().astimezone()

    for event in events:
        try:
            
            date_text = event["date"]

            try:
                # Dates from the college RSS feed
                event_date = parsedate_to_datetime(date_text)
            except (ValueError, TypeError):
                # Dates entered manually (YYYY-MM-DD HH:MM)
                event_date = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
                event_date = event_date.astimezone()


            
            if event_date >= now:
                upcoming_events.append({
                    "title": event["title"],
                    "date": event_date.strftime("%B %d, %Y at %I:%M %p"),
                    "location": event["location"],
                    "description": event["description"],
                    "sort_date": event_date
                })

        except (ValueError, TypeError, KeyError):
            continue

    # Sort upcoming events by their actual date
    upcoming_events.sort(key=lambda event: event["sort_date"])

    events = upcoming_events

    return render_template("index.html", events=events)


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(event_bp)

# Display the Add Event form and save submitted events
@app.route("/add-event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date = request.form.get("date", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not date:
            return "Event title and date are required.", 400

        # Convert HTML datetime-local to our database format
        try:
            event_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return "Invalid event date.", 400

        conn = sqlite3.connect("db/campusconnect.db")

        conn.execute("""
            INSERT INTO manual_events
            (title, date, location, description)
            VALUES (?, ?, ?, ?)
        """, (
            title,
            event_date.strftime("%Y-%m-%d %H:%M"),
            location,
            description
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_event.html")

# Automatically refresh LaGrange College events
def refresh_campus_events():
    scraper = CampusEventScraper(
        "https://www.lagrange.edu/Calendar/index.rss"
    )

    while True:
        try:
            events = scraper.parse_events(scraper.fetch_page())
            scraper.save_events(events)
            print("Automatic campus event refresh completed!")
        except Exception as error:
            print(f"Event refresh failed: {error}")

        # Wait 6 hours before checking again
        time.sleep(21600)


if __name__ == "__main__":
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        refresh_thread = threading.Thread(
            target=refresh_campus_events,
            daemon=True
        )
        refresh_thread.start()

    app.run(debug=True, port=5001)

