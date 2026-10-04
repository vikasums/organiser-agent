import os
import sqlite3
from core.config import DB_PATH, HISTORY_DIR, WORKSPACE_DIR


def init_dirs():
  os.makedirs(WORKSPACE_DIR, exist_ok=True)
  os.makedirs(HISTORY_DIR, exist_ok=True)


def init_db():
  init_dirs()
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_files (
            file_path TEXT PRIMARY KEY,
            file_size INTEGER,
            mtime REAL,
            status TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS run_history (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            summary_path TEXT,
            files_processed INTEGER
        )
    """)
  conn.commit()
  conn.close()


def get_connection():
  init_db()
  return sqlite3.connect(DB_PATH)


def save_processed_files(delta_files):
  """Checkpoints processed delta files into SQLite."""
  conn = get_connection()
  cursor = conn.cursor()
  for f in delta_files:
    cursor.execute(
        """
            INSERT OR REPLACE INTO processed_files (file_path, file_size, mtime, status)
            VALUES (?, ?, ?, 'completed')
        """,
        (f["path"], f["size"], f["mtime"]),
    )
  conn.commit()
  conn.close()
