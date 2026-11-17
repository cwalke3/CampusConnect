
# CampusConnect

CampusConnect is a Flask web application designed to help students view campus events and access public API data.

## Features

- Displays campus events from a SQLite database
- Automatically scrapes events from the LaGrange College calendar
- Allows users to manually add events
- Retrieves public API data using Python requests
- Stores API records in SQLite
- Displays API records on a webpage
- Uses HTML, CSS, Python, Flask, and SQLite

## Setting Up the Project

### 1. Install Dependencies

```bash
pip install flask requests beautifulsoup4 selenium
```

### 2. Set Up the Database

```bash
sqlite3 db/campusconnect.db < db/schema.sql
```

### 3. Add Starter Data

```bash
python3 db/seed_data.py
```

### 4. Start the Application

```bash
python3 app.py
```

### 5. Open the Website

Visit these pages in your browser:

- Home: http://127.0.0.1:5001/
- Campus Events: http://127.0.0.1:5001/events
- Public API Data: http://127.0.0.1:5001/api
- Add Event: http://127.0.0.1:5001/add-event

## API Integration

CampusConnect retrieves sample public data from JSONPlaceholder.

The API client uses Python requests to retrieve JSON data and saves the records in the SQLite database.

The records are displayed in an HTML table.

## Automatic Event Scraping

CampusConnect retrieves events from the LaGrange College calendar RSS feed.

The application stores scraped events in SQLite and automatically checks for updates every six hours while the application is running.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Requests
- BeautifulSoup
