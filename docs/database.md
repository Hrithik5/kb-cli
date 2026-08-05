# `kb` Database Schema & FTS5 Specification

## Table: `knowledge`

```sql
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT DEFAULT '',
    favorite INTEGER DEFAULT 0,
    access_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## FTS5 Virtual Table: `knowledge_fts`

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
    title,
    content,
    tags,
    content='knowledge',
    content_rowid='id',
    tokenize='porter ascii'
);
```

## Triggers

`knowledge_ai`, `knowledge_ad`, `knowledge_au` automatically synchronize `INSERT`, `DELETE`, and `UPDATE` mutations on the `knowledge` table into `knowledge_fts` in realtime.
