<!-- ========================================================= -->
<!--                          BANNER                           -->
<!-- ========================================================= -->

<p align="center">

<!-- TODO: Replace with project banner -->

<img src="assets/banner.png" width="100%" alt="kb">

</p>

<h1 align="center">
kb
</h1>

<p align="center">

⚡ Lightning-fast offline knowledge engine for developers.

Store commands, snippets, notes, and engineering knowledge in a searchable SQLite database.

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)

![License](https://img.shields.io/badge/License-MIT-green)

![CI](https://github.com/Hrithik5/kb-cli/actions/workflows/ci.yml/badge.svg)

![SQLite](https://img.shields.io/badge/SQLite-FTS5-blue)

</p>

---

# 🎬 Demo

> **TODO:** Add terminal demo GIF

<p align="center">

<img src="assets/demo.gif" width="900">

</p>

---

# Why kb?

Every developer has accumulated years of knowledge:

- Git commands
- Docker snippets
- SQL queries
- Bash one-liners
- Kubernetes commands
- AWS CLI examples
- Configuration snippets
- Troubleshooting notes

Unfortunately they're usually scattered across:

- Markdown files
- Notion
- Obsidian
- Browser bookmarks
- Terminal history
- Gists
- Sticky notes

Finding them later usually means opening multiple files and pressing **Ctrl + F** repeatedly.

**kb** replaces that workflow with an indexed local knowledge engine powered by **SQLite Full-Text Search (FTS5)**.

Everything stays local.

Everything is searchable.

Everything is instant.

---

# ✨ Features

| Feature | Status |
|----------|--------|
| Offline-first | ✅ |
| SQLite FTS5 Search | ✅ |
| Categories | ✅ |
| Tags | ✅ |
| Favorites | ✅ |
| Markdown Import | ✅ |
| JSON Export | ✅ |
| Interactive FZF | ✅ |
| Clipboard Copy | ✅ |
| Recent History | ✅ |
| Statistics | ✅ |
| Zero Cloud Services | ✅ |
| Cross Platform | ✅ |

---

# 🚀 Installation

## pip

```bash
pip install kb-cli
```

Verify installation

```bash
kb --version
```

---

# ⚡ Quick Start

Initialize the database

```bash
kb init
```

Add your first command

```bash
kb add git "git status" -t "Git Status"
```

Search

```bash
kb find git
```

Open the interactive interface

```bash
kb fzf
```

---

# 📖 Commands

| Command | Description |
|----------|-------------|
| `kb init` | Initialize database |
| `kb add` | Add new knowledge |
| `kb list` | List entries |
| `kb find` | Full-text search |
| `kb get` | View an entry |
| `kb edit` | Edit an entry |
| `kb delete` | Delete an entry |
| `kb favorite` | Mark favorite |
| `kb recent` | Recently used |
| `kb stats` | Usage statistics |
| `kb import` | Import Markdown/TXT |
| `kb export` | Export JSON/Markdown |
| `kb copy` | Copy to clipboard |
| `kb fzf` | Interactive fuzzy finder |

---

# 💡 Examples

## Save Git Commands

```bash
kb add git "git rebase -i HEAD~3" \
-t "Interactive Rebase" \
--tags git,rebase
```

Search later

```bash
kb find rebase
```

---

## Save SQL

```bash
kb add sql \
"SELECT * FROM users WHERE active = TRUE;" \
-t "Active Users"
```

---

## Save AWS Commands

```bash
kb add aws \
"aws s3 sync . s3://bucket-name"
```

---

## Export Everything

```bash
kb export markdown notes.md
```

---

# 📸 Screenshots

> **TODO:** Add screenshots

```
assets/

search.png

fzf.png

stats.png

list.png
```

---

# 🏗 Architecture

```
                 User
                  │
                  ▼
        kb CLI Interface
                  │
                  ▼
          Service Layer
                  │
                  ▼
        Repository Layer
                  │
                  ▼
     SQLite Database (FTS5)
                  │
                  ▼
          Local File System
```

---

# 📊 Project Status

Current Version

```
v0.1.1
```

Current Features

- SQLite FTS5 search
- Categories
- Tags
- Favorites
- Import / Export
- Interactive FZF
- Clipboard Support
- Statistics
- Shell Completion

---

# 🛣 Roadmap

## v0.2

- [ ] Search highlighting
- [ ] Rich preview UI
- [ ] Better FZF integration
- [ ] YAML import/export
- [ ] Colored terminal output

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run Ruff and Pytest
6. Open a Pull Request

---

# 📜 License

MIT License.

---

<p align="center">

Made with ❤️ for developers who have too many notes.

</p>
