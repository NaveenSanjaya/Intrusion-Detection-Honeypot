import requests
import sqlite3
import time

DB_PATH = 'intrusion_data.db'
BASE_URL = 'http://127.0.0.1:5000'

def reset_database():
    """Reset the database for testing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM login_attempts")
    cursor.execute("DELETE FROM blocked_ips")
    conn.commit()
    conn.close()
    print("[INFO] Database reset complete.")

def test_login_attempts():
    """Simulate login attempts for multiple users and check database entries."""
    print("[TEST] Simulating login attempts for multiple users...")
    from login_alert import log_login_attempt

    # Define test cases: (username, password, IP address)
    test_cases = [
        ("user1", "wrongpassword1", "192.168.1.101"),
        ("user2", "wrongpassword2", "192.168.1.102"),
        ("user3", "wrongpassword3", "192.168.1.103"),
        ("user1", "wrongpassword1", "192.168.1.101"),
        ("user2", "wrongpassword2", "192.168.1.102"),
        ("user3", "wrongpassword3", "192.168.1.103"),
        ("user1", "wrongpassword1", "192.168.1.101"),  # Third attempt for user1
        ("user2", "wrongpassword2", "192.168.1.102"),  # Third attempt for user2
        ("user3", "wrongpassword3", "192.168.1.103"),  # Third attempt for user3
    ]

    # Simulate login attempts
    for username, password, ip in test_cases:
        log_login_attempt(username, password, ip)
        time.sleep(0.5)  # Add delay to simulate real-world attempts

    # Check if the IPs were blocked
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    blocked_ips = []
    for _, _, ip in test_cases:
        cursor.execute("SELECT * FROM blocked_ips WHERE ip_address = ?", (ip,))
        if cursor.fetchone():
            blocked_ips.append(ip)
    conn.close()

    # Validate results
    expected_blocked_ips = {"192.168.1.101", "192.168.1.102", "192.168.1.103"}
    if set(blocked_ips) == expected_blocked_ips:
        print("[PASS] All expected IPs were successfully blocked after 3 failed attempts.")
    else:
        print("[FAIL] Some IPs were not blocked as expected.")
        print("Blocked IPs:", blocked_ips)
        
def test_api_endpoints():
    """Test API endpoints for login attempts and blocked IPs."""
    print("[TEST] Testing API endpoints...")

    # Test /api/login_attempts
    response = requests.get(f"{BASE_URL}/api/login_attempts")
    if response.status_code == 200:
        print("[PASS] /api/login_attempts endpoint is working.")
        print("Response:", response.json())
    else:
        print("[FAIL] /api/login_attempts endpoint failed.")

    # Test /api/blocked_ips
    response = requests.get(f"{BASE_URL}/api/blocked_ips")
    if response.status_code == 200:
        print("[PASS] /api/blocked_ips endpoint is working.")
        print("Response:", response.json())
    else:
        print("[FAIL] /api/blocked_ips endpoint failed.")

def test_export_data():
    """Test the export data functionality."""
    print("[TEST] Testing data export...")
    response = requests.get(f"{BASE_URL}/export_data")
    if response.status_code == 200 and "attachment; filename=exported_data.csv" in response.headers.get("Content-Disposition", ""):
        print("[PASS] Data export functionality is working.")
    else:
        print("[FAIL] Data export functionality failed.")

def main():
    """Run all tests."""
    print("[INFO] Starting system tests...")
    reset_database()
    test_login_attempts()
    test_api_endpoints()
    test_export_data()
    print("[INFO] All tests completed.")

if __name__ == "__main__":
    main()