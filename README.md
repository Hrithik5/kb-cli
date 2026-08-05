# kb — Developer Knowledge Engine ⚡

[![CI](https://github.com/hrithikchauhan/kb-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/hrithikchauhan/kb-cli/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)

> Lightning-fast, offline-first developer snippet and knowledge manager powered by SQLite FTS5.

```bash
kb add git "git branch -D feature"
kb add docker "docker compose up -d"
kb find compose
```

```
Found 1 match:

#2 [DOCKER] Start Compose
   tags: docker
   docker compose up -d
```

---

## 💡 Why `kb`?

Developers constantly reuse shell commands, configuration snippets, SQL queries, and architectural conventions. Traditional notes apps (Obsidian, Notion) are bloated, slow, and break terminal workflow. Cloud services introduce latency and privacy concerns.

`kb` is built on the **Unix philosophy**:
- 🚀 **Sub-millisecond Search**: Full-text indexing with SQLite FTS5, Porter Stemmer, and BM25 ranking.
- 🎯 **Interactive `fzf` & `tmux` Support**: Instant fuzzy finding with live snippet previews in terminal and tmux popup modals.
- 🔒 **100% Offline & Private**: Stored locally in `~/.local/share/kb/kb.db`.
- 📦 **Zero Runtime Dependencies**: Built with Python standard library. Ultra-lightweight and instant startup.
- 🐚 **Shell Autocompletion**: Built-in completions for Bash, Zsh, and Fish.
- 💻 **Cross Platform**: Seamlessly works across macOS, Linux, and Windows.

---

## 📥 Installation

### Homebrew (macOS / Linux)
```bash
brew tap hrithikchauhan/kb-cli
brew install kb
```

### From Source
```bash
git clone https://github.com/hrithikchauhan/kb-cli.git
cd kb-cli
pip install .
```

---

## ⚡ Quickstart & Usage

### 1. Initialize Database
```bash
kb init
```

### 2. Add Snippets & Notes
```bash
kb add git "git rebase --interactive HEAD~5" -t "Interactive Rebase" --tags "git,rebase"
kb add terraform "terraform state mv module.vpc module.network" -t "Rename TF State"
```

### 3. Interactive `fzf` & `tmux` Fuzzy Search 🔍
Launch interactive search with real-time preview panes. If you are inside a **tmux** session, `kb` automatically pops up a floating modal (`fzf-tmux`):

```bash
kb fzf
```

#### Bind `Ctrl+K` in Zsh / Bash
Add snippet picker directly to your shell prompt via keybinding (`scripts/kb-fzf.plugin.zsh`):
```zsh
source /path/to/kb-cli/scripts/kb-fzf.plugin.zsh
```
Pressing **`Ctrl+K`** in your shell opens the `fzf` popup and inserts the selected snippet into your terminal prompt!

### 4. Full-Text Search (FTS5)
```bash
kb find rebase
```

### 5. Copy Directly to System Clipboard
```bash
kb copy 1
# Output: ✔ Copied snippet #1 to clipboard!
```

---

## 🐚 Shell Autocompletion

Generate autocompletion scripts dynamically for your shell:

```bash
# Zsh
kb completion zsh > ~/.zsh/completions/_kb

# Bash
kb completion bash > ~/.local/share/bash-completion/completions/kb

# Fish
kb completion fish > ~/.config/fish/completions/kb.fish
```

---

## 📁 Import & Export Workflows

### Bulk Import Markdown / Plain Text
```bash
kb import markdown ~/Notes/git_cheatsheet.md -c git
kb import txt ~/docker-commands.txt -c docker
```

### Export to JSON or Markdown
```bash
kb export json ~/backup/kb_export.json
kb export markdown ~/backup/kb_notes.md
kb export backup ~/backup/kb.db
```

---

## ⚙️ Configuration

`kb` automatically reads settings from `~/.config/kb/config.toml`:

```toml
# ~/.config/kb/config.toml
database = "~/.local/share/kb/kb.db"
editor = "nvim"
default_limit = 10
theme = "nord"
pager = "less"
```

---

## 🏗️ Architecture

```
┌──────────────────┐
│      CLI         │ kb argparse CLI Router
└─────────┬────────┘
          ▼
┌──────────────────┐
│  Command Layer   │ add, find, fzf, edit, list, import...
└─────────┬────────┘
          ▼
┌──────────────────┐
│  Service Layer   │ Business validation & logic
└─────────┬────────┘
          ▼
┌──────────────────┐
│ Repository Layer │ SQLite queries & FTS5 BM25 ranking
└─────────┬────────┘
          ▼
┌──────────────────┐
│  SQLite + FTS5   │ Embedded FTS5 database engine
└─────────┬────────┘
          ▼
┌──────────────────┐
│ fzf / fzf-tmux   │ Interactive popup preview integration
└──────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for setup and development instructions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
