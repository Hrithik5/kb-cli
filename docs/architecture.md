# `kb` Architecture Guide

## System Overview

`kb` is organized into five strict, decoupled layers:

1. **CLI Layer (`kb/cli.py`, `kb/main.py`)**: Responsible for command-line argument parsing (`argparse`), exit code propagation, signal handling, and routing.
2. **Command Layer (`kb/commands/`)**: Subcommand implementations (`init`, `add`, `find`, `list`, `edit`, `delete`, `import`, `export`, `stats`, `favorite`, `recent`, `copy`). Translates CLI options into service calls and formats output.
3. **Service Layer (`kb/services/`)**: Enforces business logic, data validation, normalization, and import/export parsing (`KnowledgeService`, `ImportExportService`).
4. **Repository Layer (`kb/repositories/`)**: Encapsulates raw SQL queries and FTS5 full-text search (`KnowledgeRepository`).
5. **Storage Layer (`kb/database.py`, `kb/schema.sql`)**: Manages SQLite connections, FTS5 virtual table synchronization, and transaction lifecycles.

## Layer Communication Rules

- **CLI → Commands → Services → Repositories → SQLite**
- Commands NEVER execute SQL queries directly.
- Repositories NEVER write to `sys.stdout` or stdout/stderr.
- Services NEVER parse CLI arguments.
- CLI NEVER contains business domain logic.

## Data Flow: `kb find compose`

```
1. CLI receives `kb find compose`
2. cli.py instantiates FindCommand with KnowledgeService
3. FindCommand calls service.find_items(query="compose")
4. KnowledgeService normalizes query and delegates to KnowledgeRepository.find()
5. KnowledgeRepository executes SQL MATCH against `knowledge_fts` virtual table
6. SQLite returns BM25-ranked rows
7. Repositories map rows to KnowledgeItem dataclasses
8. Formatter renders colored ANSI output to terminal
```
