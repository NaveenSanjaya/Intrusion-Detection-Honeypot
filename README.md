# 🛡️ Intrusion Detection & Honeypot System with Analytics Dashboard

A lightweight Intrusion Detection System (IDS) and Honeypot built using Python and Flask. This project logs unauthorized login attempts, blocks suspicious IPs, and provides a modern web dashboard for intrusion analytics. It optionally sends real-time alerts via Telegram.

## 🔧 Features

- 🔐 **Login Honeypot** – Captures all login attempts.
- 📊 **Analytics Dashboard** – View recent login attempts and blocked IPs via a clean UI.
- 📁 **SQLite Logging** – Stores login and blocking activity locally.
- 🚫 **IP Blocking** – Automatically blocks brute-force attempts.
- 📱 **Telegram Alerts** – Optional notifications for login attempts.

---

## 📂 Project Structure

Intrusion-Detection-Honeypot/ ├── app.py # Flask backend ├── database_setup.py # DB schema setup script ├── intrusion_log.py # Logs login attempts ├── static/ │ └── styles.css # Dashboard styling ├── templates/ │ └── index.html # Dashboard frontend ├── intrusion_data.db # SQLite DB (created at runtime) ├── config.py # Telegram config (optional) └── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Intrusion-Detection-Honeypot.git
cd Intrusion-Detection-Honeypot
2. Create a Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Setup the Database
bash
Copy
Edit
python database_setup.py
This script creates:

login_attempts table

blocked_ips table

5. Run the Flask App
bash
Copy
Edit
python app.py
Open your browser and visit:
📍 http://127.0.0.1:5000

🛠️ Simulate Intruder Activity
Use the following command or a script to simulate login attempts:

bash
Copy
Edit
python intrusion_log.py --username test --password wrongpass --ip 192.168.1.100
🔔 Optional: Telegram Alerts
To enable Telegram alerts:

Get your Telegram bot token from BotFather.

Get your chat ID from @userinfobot.

Create a config.py file:

python
Copy
Edit
TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
TELEGRAM_CHAT_ID = 'your_chat_id_here'
The app will automatically send messages on new login attempts.

📊 Dashboard Preview
Recent Login Attempts (username, IP, time, status)

Blocked IPs (with timestamps)

Auto-refreshing via AJAX

<!-- You can add a screenshot of your dashboard here --> <!-- ![Dashboard Screenshot](https://your-screenshot-link.com/dashboard.png) -->
⚙️ API Endpoints
Endpoint	Method	Description
/api/login_attempts	GET	Returns last 10 login attempts
/api/blocked_ips	GET	Returns last 10 blocked IPs
🧠 Future Enhancements
Add geolocation using IP

Email alert support

Admin login and panel

Brute-force threshold customization

🤝 Contributing
Pull requests are welcome! If you have suggestions or want to enhance the dashboard or detection mechanism, feel free to fork the project.

📜 License
MIT License – feel free to use and modify for your projects!

👤 Author
Naveen
📫 Email me | 🌐 Portfolio

python
Copy
Edit

---

Let me know if you'd like the `requirements.txt` content too or if you're preparing this for submission and need a polished zipped bundle!