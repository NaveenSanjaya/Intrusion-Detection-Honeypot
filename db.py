import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('intrusion_data.db')
cursor = conn.cursor()

# Create login_attempts table with ip_address and status column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        ip_address TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT
    )
''')

# Create blocked_ips table with blocked_timestamp column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blocked_ips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE,
        blocked_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully!")