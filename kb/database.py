import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    """Manages SQLite database connections and schema initialization."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_db_dir()
        self._conn = None

    def _ensure_db_dir(self):
        if self.db_path != Path(":memory:"):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")
        return self._conn

    def init_schema(self, schema_path: Optional[Path] = None):
        """Executes the schema SQL script to set up tables, FTS5 virtual table, and triggers."""
        if schema_path is None:
            schema_path = Path(__file__).parent / "schema.sql"

        schema_sql = schema_path.read_text(encoding="utf-8")
        conn = self.get_connection()
        conn.executescript(schema_sql)
        conn.commit()
    def check_fts5_supported(self) -> bool:
        """Verifies if SQLite compile option includes FTS5."""
        try:
            conn = self.get_connection()
            cursor = conn.execute("PRAGMA compile_options;")
            options = [row[0] for row in cursor.fetchall()]
            if any("ENABLE_FTS5" in opt for opt in options):
                return True
            # Fallback test via virtual table query
            conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _fts5_test USING fts5(c);")
            conn.execute("DROP TABLE _fts5_test;")
            return True
        except sqlite3.OperationalError:
            return False
