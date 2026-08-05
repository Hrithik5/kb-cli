# `kb` Product Roadmap

## v0.1 — Core Foundation
- [x] Layered architecture (CLI -> Services -> Repositories -> SQLite FTS5)
- [x] `kb init`, `kb add`, `kb find`, `kb list`, `kb edit`, `kb delete`
- [x] Zero third-party runtime dependencies

## v0.2 — Quality of Life & Import/Export
- [x] Markdown & Plain text file importers
- [x] JSON, Markdown, and SQLite export & backup
- [x] Clipboard integration (`kb copy`)
- [x] Favorites & Statistics tracking (`kb favorite`, `kb stats`, `kb recent`)

## v0.3 — Packaging, Shell & Terminal Integration
- [x] Homebrew formula (`brew install kb`)
- [x] Shell completion scripts (`kb completion zsh|bash|fish`)
- [x] Synergistic integration with terminal fuzzy finders (`kb fzf` with `tmux` popup support)
- [ ] Publish to PyPI (`pip install kb-cli`)

## v1.0 — Plugin Ecosystem
- [ ] Plugin API for custom importers (Obsidian, Notion, GitHub Gists)
