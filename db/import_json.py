"""Import the legacy JSON records into the SQLite project database."""
import json
import sqlite3
from typing import Any

from db.database import DB_PATH, PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"


def read_json(filename: str) -> list[dict[str, Any]]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        return [dict(id=int(key), **record) for key, record in value.items()]
    return value if isinstance(value, list) else []


def import_json() -> None:
    """Create the schema and replace table contents from the JSON sources."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8-sig"))
        with connection:
            tables = ("repair_requests", "services", "specialists", "clients")
            for table in tables:
                connection.execute(f"DELETE FROM {table}")
            connection.executemany(
                "INSERT INTO clients (id, name, phone) VALUES (?, ?, ?)",
                [(r["id"], r["name"], r["phone"])
                 for r in read_json("clients.json")],
            )
            connection.executemany(
                "INSERT INTO specialists (id, name, specialization, rate) "
                "VALUES (?, ?, ?, ?)",
                [(r["id"], r["name"], r["specialization"], r["rate"])
                 for r in read_json("specialists.json")],
            )
            connection.executemany(
                "INSERT INTO services "
                "(id, name, required_specialization, hours) "
                "VALUES (?, ?, ?, ?)",
                [(r["id"], r["name"], r["required_specialization"], r["hours"])
                 for r in read_json("services.json")],
            )
            connection.executemany(
                "INSERT INTO repair_requests "
                "(id, client_id, specialist_id, service_id, request_date, "
                "is_cancelled) VALUES (?, ?, ?, ?, ?, ?)",
                [(r["id"], r["client_id"], r["specialist_id"],
                  r["service_id"], r.get("date", r.get("request_date")),
                  int(r.get("is_cancelled", r.get("status") == "отменена")))
                 for r in read_json("requests.json")],
            )
    finally:
        connection.close()


if __name__ == "__main__":
    import_json()
    print(f"JSON импортирован в {DB_PATH}")
