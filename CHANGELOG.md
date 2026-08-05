# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-05

### Added
- Core CLI framework with `argparse` routing (`kb`).
- SQLite FTS5 database integration with Porter stemming and BM25 search ranking.
- Subcommands:
  - `kb init`: Database and config file initialization.
  - `kb add`: Insert new snippets and notes with tags and titles.
  - `kb find`: Full-text search across title, content, and tags.
  - `kb list`: Browse entries by category or limit.
  - `kb edit`: Update existing snippets.
  - `kb delete`: Remove entries by ID.
  - `kb import`: Bulk import Markdown and plain text files.
  - `kb export`: Export database entries to JSON, Markdown, or SQLite backup.
  - `kb stats`: Display category breakdown and access count metrics.
  - `kb favorite`: Flag favorite snippets and filter by favorites.
  - `kb recent`: Display recently created or modified items.
  - `kb copy`: Copy snippet directly to system clipboard.
- Zero third-party runtime dependency design.
- Full test suite supporting standard library unittest and pytest.
