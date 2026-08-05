from pathlib import Path
from kb.database import Database


def test_in_memory_database():
    db = Database(Path(":memory:"))
    assert db.db_path == Path(":memory:")
    conn = db.get_connection()
    assert conn is not None
    conn.close()


def test_schema_initialization():
    db = Database(Path(":memory:"))
    db.init_schema()

    with db.get_connection() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        assert "knowledge" in tables
        assert "knowledge_fts" in tables


def test_fts5_support():
    db = Database(Path(":memory:"))
    assert db.check_fts5_supported() is True
