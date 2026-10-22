"""SQLite access helpers for the repair service."""
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "repair_service.sqlite3"


def get_connection() -> sqlite3.Connection:
    """Open the project database with foreign-key checks enabled."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
