import logging
import asyncio
import subprocess
import sqlite3
from telegram import Bot
from telegram.error import TelegramError

# Set up logging
logging.basicConfig(filename='login_attempts.log', level=logging.INFO, format='%(asctime)s - %(message)s')
blocked_ips_log = 'blocked_ips.log'
DB_PATH = 'intrusion_data.db'

# Telegram Bot setup
TELEGRAM_API_KEY = '7731626441:AAFoUs4f7h_QeIexuccDh4ZeBI42CGMsiOo'
CHAT_ID = '1358202646'
bot = Bot(token=TELEGRAM_API_KEY)

# Track failed attempts per IP
failed_attempts = {}
BLOCK_THRESHOLD = 3  # Block IP after 3 failed attempts

# Initialize SQLite Database
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS login_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        password TEXT,
                        ip_address TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip_address TEXT UNIQUE,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

async def send_telegram_alert(message):
    """Send an alert via Telegram."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
    except TelegramError as e:
        logging.error(f"Error sending alert: {e}")

def block_ip(ip_address):
    """Block an IP using UFW (or iptables as fallback)."""
    try:
        subprocess.run(["sudo", "ufw", "deny", "from", ip_address, "to", "any"], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"], check=True)
    log_blocked_ip(ip_address)

# Update log_login_attempt to include 'status' column
def log_login_attempt(username, password, src_ip):
    """Log login attempts into file and database."""
    log_message = f"\U0001F510 Login attempt [Username: {username}, Password: {password}] from IP {src_ip}"
    logging.info(log_message)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    status = "failed"  # Default status for failed attempts
    cursor.execute("INSERT INTO login_attempts (username, password, ip_address, status) VALUES (?, ?, ?, ?)", 
                   (username, password, src_ip, status))
    conn.commit()
    conn.close()
    
    failed_attempts[src_ip] = failed_attempts.get(src_ip, 0) + 1
    
    if failed_attempts[src_ip] >= BLOCK_THRESHOLD:
        block_ip(src_ip)
    else:
        message = f"\U0001F6A8 <b>Failed Login Attempt</b>\n👤 <b>Username:</b> <code>{username}</code>\n🔑 <b>Password:</b> <code>{password}</code>\n🌐 <b>IP:</b> <code>{src_ip}</code>\n⚠️ Attempts: {failed_attempts[src_ip]}/{BLOCK_THRESHOLD}"
        asyncio.run(send_telegram_alert(message))

# Update log_blocked_ip to use 'blocked_timestamp'
def log_blocked_ip(ip_address):
    """Log blocked IPs into file and database."""
    with open(blocked_ips_log, 'a') as f:
        f.write(f"{ip_address} - Blocked\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO blocked_ips (ip_address) VALUES (?)", (ip_address,))
    conn.commit()
    conn.close()
    
    message = f"\U0001F6A8 <b>ALERT!</b>\n\U0001F534 IP <code>{ip_address}</code> has been <b>BLOCKED</b> after multiple failed login attempts!"
    asyncio.run(send_telegram_alert(message))

# Simulate an intruder login attempt
def simulate_intruder():
    username = "fakeuser"
    password = "fakepassword"
    src_ip = "192.168.137.78"
    log_login_attempt(username, password, src_ip)

# Initialize database on script start
initialize_db()

# Call simulate_intruder to test
if __name__ == "__main__":
    simulate_intruder()
    simulate_intruder()
    simulate_intruder()
