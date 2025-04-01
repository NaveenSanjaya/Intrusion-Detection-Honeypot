from flask import Flask, render_template, jsonify, make_response
import sqlite3
import csv
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    try:
        conn = sqlite3.connect('intrusion_data.db')
        conn.row_factory = sqlite3.Row
        logging.debug("Database connection established.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/login_attempts')
def api_login_attempts():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, ip_address, timestamp, status FROM login_attempts ORDER BY timestamp DESC LIMIT 10')
        login_attempts = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in login_attempts])
    return jsonify({"error": "Database connection failed"}), 500

@app.route('/api/blocked_ips')
def api_blocked_ips():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT ip_address, blocked_timestamp FROM blocked_ips ORDER BY blocked_timestamp DESC LIMIT 10')
        blocked_ips = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in blocked_ips])
    return jsonify({"error": "Database connection failed"}), 500

@app.route('/export_data')
def export_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()

    # Fetch login attempts
    cursor.execute('SELECT username, password, ip_address, timestamp, status FROM login_attempts')
    login_attempts = cursor.fetchall()

    # Fetch blocked IPs
    cursor.execute('SELECT ip_address, blocked_timestamp FROM blocked_ips')
    blocked_ips = cursor.fetchall()
    conn.close()

    # Prepare CSV data
    csv_data = []
    csv_data.append(["Login Attempts"])
    csv_data.append(["Username", "Password", "IP Address", "Timestamp", "Status"])
    csv_data.extend([list(row) for row in login_attempts])

    csv_data.append([""])  # Spacer
    csv_data.append(["Blocked IPs"])
    csv_data.append(["IP Address", "Blocked Since"])
    csv_data.extend([list(row) for row in blocked_ips])

    # Serve as CSV
    response = make_response()
    response.headers["Content-Disposition"] = "attachment; filename=exported_data.csv"
    response.headers["Content-type"] = "text/csv"

    writer = csv.writer(response)
    writer.writerows(csv_data)
    return response

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)
