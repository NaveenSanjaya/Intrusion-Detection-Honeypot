# Intrusion Detection Honeypot

The **Intrusion Detection Honeypot** is a security-focused application designed to monitor and log unauthorized login attempts, block malicious IPs, and provide real-time analytics through a web-based dashboard. It integrates with Telegram for instant alerts and supports exporting data for further analysis.

---

## Features

- **Real-Time Monitoring**: Tracks login attempts and blocked IPs.
- **IP Blocking**: Automatically blocks IPs after a configurable number of failed login attempts.
- **Web Dashboard**: Displays login attempts and blocked IPs with dynamic charts and tables.
- **Telegram Alerts**: Sends instant alerts for failed login attempts and blocked IPs.
- **Data Export**: Allows exporting login and blocked IP data as a CSV file.
- **Customizable Thresholds**: Configure the number of failed attempts before blocking an IP.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- SQLite (pre-installed with Python)
- Flask
- Chart.js (for dynamic charts)
- jQuery
- UFW or iptables (for IP blocking)
- Telegram Bot API Key and Chat ID

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/Intrusion-Detection-Honeypot.git
   cd Intrusion-Detection-Honeypot

Install Dependencies: Install the required Python packages:

Set Up the Database: Initialize the SQLite database:

Configure Telegram Bot: Update the TELEGRAM_API_KEY and CHAT_ID in login_alert.py with your Telegram Bot API key and chat ID.

Usage
Start the Flask Application: Run the Flask app to start the web dashboard:

Simulate Intrusions: Use the test_system.py script to simulate login attempts and blocked IPs:

Access the Dashboard: Open your browser and navigate to:

Export Data: Click the "Export Data to CSV" button on the dashboard to download the data.

Configuration
Telegram Bot Setup
Create a Telegram bot using BotFather.
Obtain the API key and update the following variables in login_alert.py:
Blocking Threshold
Modify the BLOCK_THRESHOLD in login_alert.py to change the number of failed attempts before blocking an IP:

File Structure
API Endpoints
The application provides the following API endpoints:

Login Attempts:

Returns the latest login attempts in JSON format.

Blocked IPs:

Returns the list of blocked IPs in JSON format.

Export Data:

Exports login attempts and blocked IPs as a CSV file.

Security Considerations
Telegram API Key: Do not expose your Telegram API key in public repositories. Use environment variables or a .env file to store sensitive information.
IP Blocking: Ensure UFW or iptables is properly configured and running on your system.
Database Security: Protect the intrusion_data.db file from unauthorized access.
Troubleshooting
Charts Not Updating:

Ensure the /api/login_attempts and /api/blocked_ips endpoints are returning valid data.
Check the JavaScript console for errors.
Telegram Alerts Not Working:

Verify the TELEGRAM_API_KEY and CHAT_ID are correct.
Check the Telegram bot permissions.
Database Issues:

Ensure the intrusion_data.db file exists and is initialized using db.py.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask for the web framework.
Chart.js for dynamic charts.
Telegram Bot API for instant alerts.
Disclaimer
This project is for educational purposes only. Use it responsibly and ensure compliance with local laws and regulations.

