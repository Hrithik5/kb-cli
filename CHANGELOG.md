# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-08-08

### Added

- Interactive REPL (`kb`) for managing snippets without leaving the terminal.
- Persistent command history for the interactive shell.
- Tab completion for shell commands.
- Command aliases (`ls`, `q`, `?`) for a smoother interactive experience.
- Colored interactive prompt and improved terminal formatting.
- Enhanced `fzf` interface with:
  - Live preview window
  - tmux popup support
  - Rich metadata display
  - Keyboard-first workflow
  - Optional syntax-highlighted previews using `bat`
- Improved clipboard integration.
- Richer CLI output with consistent ANSI formatting.
- Better search experience with improved FTS query handling and fallback search.
- Expanded documentation with a redesigned README, demo GIF support, architecture overview, and roadmap.

### Improved

- Refactored repository search logic for more reliable SQLite FTS5 queries.
- Improved fallback `LIKE` search for malformed FTS queries.
- Better command organization across CLI modules.
- Cleaner output formatting across all commands.
- Improved shell usability and developer experience.
- Enhanced interactive navigation throughout the CLI.

### Fixed

- Fixed preview execution inside `fzf` when running in development environments.
- Fixed command execution inside the interactive shell.
- Fixed several Ruff linting issues.
- Improved error handling across CLI commands.
- Various bug fixes and code cleanup.

---

## [0.1.0] - 2026-08-05

### Added

- Initial release of **kb**.
- Core CLI framework with `argparse` routing.
- SQLite FTS5 database integration with Porter stemming and BM25 ranking.
- Offline-first knowledge storage.
- Support for categories, tags, favorites, and usage tracking.
- Subcommands:
  - `kb init`
  - `kb add`
  - `kb find`
  - `kb list`
  - `kb get`
  - `kb edit`
  - `kb delete`
  - `kb import`
  - `kb export`
  - `kb stats`
  - `kb favorite`
  - `kb recent`
  - `kb copy`
- JSON and Markdown import/export support.
- Clipboard integration.
- Shell completion support.
- Zero third-party runtime dependency design.
- Automated test suite using `pytest`.
