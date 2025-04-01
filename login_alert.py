import logging
import asyncio
import time
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from telegram import Bot
from telegram.error import TelegramError

# Telegram Bot setup
TELEGRAM_API_KEY = '7731626441:AAFoUs4f7h_QeIexuccDh4ZeBI42CGMsiOo'
CHAT_ID = '1358202646'
bot = Bot(token=TELEGRAM_API_KEY)

# Configure logging with rotation
log_file = 'login_attempts.log'
handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=5)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Track failed login attempts per IP
failed_attempts = defaultdict(list)
FAILED_THRESHOLD = 3  # Trigger alert after 3 failed attempts
TIME_WINDOW = 300  # 5-minute window

async def send_telegram_alert(message):
    """Send an alert message via Telegram."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except TelegramError as e:
        logging.error(f"Error sending alert: {e}")

def log_login_attempt(username, password, src_ip, success=False):
    """Log login attempts and trigger alerts on repeated failures."""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    log_message = f"{status} Login Attempt [User: `{username}`, Password: `{password}`] from `{src_ip}`"
    
    # Log to file
    logging.info(log_message)

    # If failed, track the attempt
    if not success:
        track_failed_attempt(src_ip)

    # Send a Telegram alert for all attempts (optional, remove if you only want alerts for failures)
    asyncio.run(send_telegram_alert(log_message))

def track_failed_attempt(ip_address):
    """Track failed login attempts and trigger an alert if the threshold is exceeded."""
    current_time = time.time()
    
    # Store the attempt timestamp
    failed_attempts[ip_address].append(current_time)

    # Keep only attempts within the last TIME_WINDOW (5 minutes)
    failed_attempts[ip_address] = [t for t in failed_attempts[ip_address] if current_time - t < TIME_WINDOW]

    # If threshold exceeded, send an alert
    if len(failed_attempts[ip_address]) >= FAILED_THRESHOLD:
        alert_message = (
            f"🚨 *Repeated Failed Login Attempts Detected!* 🚨\n\n"
            f"📍 *IP Address:* `{ip_address}`\n"
            f"❌ *Failed Attempts:* `{len(failed_attempts[ip_address])}`\n"
            f"⏳ *Time Window:* Last {TIME_WINDOW//60} minutes\n\n"
            f"⚠️ Consider blocking this IP!"
        )
        asyncio.run(send_telegram_alert(alert_message))

# Simulate login attempts
def simulate_intruder():
    """Simulates an intruder with multiple login attempts."""
    attempts = [
        ("fakeuser1", "wrongpass", "192.168.137.78"),
        ("fakeuser2", "123456", "192.168.137.78"),
        ("admin", "admin123", "192.168.137.78"),
        ("root", "toor", "192.168.137.78"),  # This will trigger the alert
    ]

    for username, password, src_ip in attempts:
        log_login_attempt(username, password, src_ip, success=False)
        time.sleep(2)  # Simulating a time gap between login attempts

# Call simulate_intruder to test
if __name__ == "__main__":
    simulate_intruder()
