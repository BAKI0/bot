import os
import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL:
        print("DATABASE_URL is missing. Please set it in .env.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        username TEXT,
        karma INTEGER DEFAULT 0,
        positive_streak INTEGER DEFAULT 0,
        join_date TEXT,
        message_count INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agreements (
        user_id BIGINT PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        agreed BOOLEAN,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strikes (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        reason TEXT,
        timestamp TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flood_log (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        timestamp TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully on Supabase (PostgreSQL).")
