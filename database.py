import sqlite3

conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT,
    details TEXT
)
""")

conn.commit()
conn.close()
