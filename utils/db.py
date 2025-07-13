import sqlite3
import hashlib


def get_db_connection():
    return sqlite3.connect('rayfield.db')


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect('rayfield.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE,
                  password TEXT,
                  role TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS assets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  type TEXT,
                  status TEXT,
                  location TEXT,
                  alerts INTEGER DEFAULT 0)''')

    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  asset_id INTEGER,
                  severity TEXT,
                  detected TEXT,
                  metric TEXT,
                  likely_cause TEXT,
                  suggested_action TEXT,
                  FOREIGN KEY(asset_id) REFERENCES assets(id))''')

    # Insert sample data if empty
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        sample_users = [
            ('admin@rayfield.com', hash_password('admin123'), 'Admin'),
            ('ops@rayfield.com', hash_password('password123'), 'Operations Manager'),
            ('exec@rayfield.com', hash_password('password123'), 'Executive Director'),
            ('analyst@rayfield.com', hash_password('password123'), 'Analyst'),
            ('tech@rayfield.com', hash_password('password123'), 'Technician')
        ]
        c.executemany("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", sample_users)

    if c.execute("SELECT COUNT(*) FROM assets").fetchone()[0] == 0:
        sample_assets = [
            ('Solar Plant A', 'Solar', 'Normal', 'Texas', 0),
            ('Wind Turbine B', 'Wind', 'Warning', 'Missouri', 2),
            ('Battery Storage C', 'Battery', 'Critical', 'Georgia', 4),
            ('Wind Turbine D', 'Wind', 'Normal', 'Utah', 0),
            ('Solar Plant E', 'Solar', 'Normal', 'New York', 1)
        ]
        c.executemany("INSERT INTO assets (name, type, status, location, alerts) VALUES (?, ?, ?, ?, ?)", sample_assets)

    if c.execute("SELECT COUNT(*) FROM alerts").fetchone()[0] == 0:
        sample_alerts = [
            (2, 'High', '2025-06-15 08:30', 'Vibration 7.2mm/s', 'Bearing wear', 'Inspect + lubricate'),
            (3, 'Critical', '2025-06-15 09:15', 'Temperature 142°C', 'Cooling failure', 'Emergency shutdown'),
            (2, 'Medium', '2025-06-14 14:20', 'Power fluctuation', 'Grid instability', 'Monitor closely')
        ]
        c.executemany(
            "INSERT INTO alerts (asset_id, severity, detected, metric, likely_cause, suggested_action) VALUES (?, ?, ?, ?, ?, ?)",
            sample_alerts)

    c.execute('''CREATE TABLE IF NOT EXISTS solar_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  generation_kw REAL,
                  is_anomaly INTEGER DEFAULT 0)''')

    c.execute('''CREATE TABLE IF NOT EXISTS solar_alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  generation_kw REAL,
                  deviation REAL,
                  detected TEXT)''')

    conn.commit()
    conn.close()