from datetime import datetime

from kb.database import Database
from kb.models.knowledge import KnowledgeItem


class KnowledgeRepository:
    """Handles raw SQL and FTS5 full-text search operations on SQLite."""

    def __init__(self, db: Database):
        self.db = db

    def _row_to_item(self, row) -> KnowledgeItem:
        tags_raw = row["tags"] or ""
        tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]
        return KnowledgeItem(
            id=row["id"],
            category=row["category"],
            title=row["title"],
            content=row["content"],
            tags=tags_list,
            favorite=bool(row["favorite"]),
            access_count=row["access_count"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def add(self, item: KnowledgeItem) -> KnowledgeItem:
        tags_str = item.tags_str
        now = datetime.now().isoformat()
        sql = """
            INSERT INTO knowledge (category, title, content, tags, favorite, access_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                item.category,
                item.title,
                item.content,
                tags_str,
                1 if item.favorite else 0,
                item.access_count,
                item.created_at or now,
                item.updated_at or now
            ))
            item.id = cursor.lastrowid
        return item

    def get_by_id(self, item_id: int) -> KnowledgeItem | None:
        sql = "SELECT * FROM knowledge WHERE id = ?;"
        with self.db.get_connection() as conn:
            row = conn.execute(sql, (item_id,)).fetchone()
            if row:
                return self._row_to_item(row)
        return None

    def find(self, query: str, limit: int = 10, category: str | None = None) -> list[KnowledgeItem]:
        """Performs FTS5 search using BM25 ranking."""
        # Sanitize query for FTS5 syntax
        fts_query = self._format_fts_query(query)
        if not fts_query:
            return self.list_all(limit=limit, category=category)

        if category:
            sql = """
                SELECT k.*, fts.rank
                JOIN knowledge_fts fts ON k.id = fts.rowid
                FROM knowledge k
                WHERE knowledge_fts MATCH ? AND k.category = ?
                ORDER BY fts.rank
                LIMIT ?;
            """
            params = (fts_query, category, limit)
        else:
            sql = """
                SELECT k.*, fts.rank
                FROM knowledge k
                JOIN knowledge_fts fts ON k.id = fts.rowid
                WHERE knowledge_fts MATCH ?
                ORDER BY fts.rank
                LIMIT ?;
            """
            params = (fts_query, limit)

        try:
            with self.db.get_connection() as conn:
                rows = conn.execute(sql, params).fetchall()
                return [self._row_to_item(r) for r in rows]
        except Exception:
            # Fallback to LIKE search if FTS syntax error
            return self._like_search(query, limit, category)

    def _format_fts_query(self, query: str) -> str:
        """Sanitizes user input into valid FTS5 tokens."""
        tokens = [t.strip('\'"*():') for t in query.split() if t.strip('\'"*():')]
        if not tokens:
            return ""
        # Append wildcard to the last token for prefix matching
        formatted = " ".join(tokens[:-1] + [f"{tokens[-1]}*"]) if len(tokens) > 1 else f"{tokens[0]}*"
        return formatted

    def _like_search(self, query: str, limit: int = 10, category: str | None = None) -> list[KnowledgeItem]:
        pattern = f"%{query}%"
        if category:
            sql = """
                SELECT * FROM knowledge
                WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?) AND category = ?
                ORDER BY updated_at DESC
                LIMIT ?;
            """
            params = (pattern, pattern, pattern, category, limit)
        else:
            sql = """
                SELECT * FROM knowledge
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?;
            """
            params = (pattern, pattern, pattern, limit)

        with self.db.get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_item(r) for r in rows]

    def list_all(self, limit: int = 20, category: str | None = None) -> list[KnowledgeItem]:
        if category:
            sql = "SELECT * FROM knowledge WHERE category = ? ORDER BY updated_at DESC LIMIT ?;"
            params = (category, limit)
        else:
            sql = "SELECT * FROM knowledge ORDER BY updated_at DESC LIMIT ?;"
            params = (limit,)

        with self.db.get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_item(r) for r in rows]

    def update(self, item: KnowledgeItem) -> KnowledgeItem:
        item.updated_at = datetime.now().isoformat()
        sql = """
            UPDATE knowledge
            SET category = ?, title = ?, content = ?, tags = ?, favorite = ?, updated_at = ?
            WHERE id = ?;
        """
        with self.db.get_connection() as conn:
            conn.execute(sql, (
                item.category,
                item.title,
                item.content,
                item.tags_str,
                1 if item.favorite else 0,
                item.updated_at,
                item.id
            ))
        return item

    def delete(self, item_id: int) -> bool:
        sql = "DELETE FROM knowledge WHERE id = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (item_id,))
            return cursor.rowcount > 0

    def increment_access(self, item_id: int) -> None:
        sql = "UPDATE knowledge SET access_count = access_count + 1 WHERE id = ?;"
        with self.db.get_connection() as conn:
            conn.execute(sql, (item_id,))

    def toggle_favorite(self, item_id: int) -> bool | None:
        item = self.get_by_id(item_id)
        if not item:
            return None
        new_fav = not item.favorite
        sql = "UPDATE knowledge SET favorite = ? WHERE id = ?;"
        with self.db.get_connection() as conn:
            conn.execute(sql, (1 if new_fav else 0, item_id))
        return new_fav

    def get_recent(self, limit: int = 10) -> list[KnowledgeItem]:
        sql = "SELECT * FROM knowledge ORDER BY updated_at DESC LIMIT ?;"
        with self.db.get_connection() as conn:
            rows = conn.execute(sql, (limit,)).fetchall()
            return [self._row_to_item(r) for r in rows]

    def get_favorites(self, limit: int = 20) -> list[KnowledgeItem]:
        sql = "SELECT * FROM knowledge WHERE favorite = 1 ORDER BY updated_at DESC LIMIT ?;"
        with self.db.get_connection() as conn:
            rows = conn.execute(sql, (limit,)).fetchall()
            return [self._row_to_item(r) for r in rows]

    def get_stats(self) -> dict:
        sql_total = "SELECT COUNT(*) FROM knowledge;"
        sql_categories = "SELECT category, COUNT(*) as count FROM knowledge GROUP BY category ORDER BY count DESC;"
        sql_favs = "SELECT COUNT(*) FROM knowledge WHERE favorite = 1;"
        sql_most_accessed = "SELECT * FROM knowledge ORDER BY access_count DESC LIMIT 5;"

        with self.db.get_connection() as conn:
            total = conn.execute(sql_total).fetchone()[0]
            favs = conn.execute(sql_favs).fetchone()[0]
            cat_rows = conn.execute(sql_categories).fetchall()
            categories = {r["category"]: r["count"] for r in cat_rows}
            accessed_rows = conn.execute(sql_most_accessed).fetchall()
            most_accessed = [self._row_to_item(r) for r in accessed_rows if r["access_count"] > 0]

        return {
            "total_items": total,
            "favorite_items": favs,
            "categories": categories,
            "most_accessed": most_accessed
        }
