import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "truthguard.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        prediction TEXT,
        confidence REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_prediction(text, prediction, confidence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (text, prediction, confidence, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        text,
        prediction,
        confidence,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def fetch_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM predictions
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='real'"
    )
    real_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='fake'"
    )
    fake_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(confidence) FROM predictions"
    )
    avg_confidence = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "real": real_count,
        "fake": fake_count,
        "avg_confidence": round((avg_confidence or 0) * 100, 2)
    }