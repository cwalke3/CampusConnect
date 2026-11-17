
from flask import Blueprint, render_template
import sqlite3

api_bp = Blueprint("api", __name__)

# Display public API data
@api_bp.route("/api")
def api():
    conn = sqlite3.connect("db/campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Retrieve API records from the database
    cursor.execute("SELECT * FROM api_data")
    api_data = cursor.fetchall()

    conn.close()

    return render_template("api.html", api_data=api_data)
