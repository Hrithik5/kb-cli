# `kb` CLI Reference

## Available Commands

| Command | Description | Syntax / Flags |
|---|---|---|
| `init` | Initialize DB & config | `kb init [--force]` |
| `add` | Add entry | `kb add <category> <content> [-t TITLE] [--tags TAGS]` |
| `find` | Full-text search | `kb find [query] [-c CATEGORY] [-l LIMIT]` |
| `list` | List entries | `kb list [-c CATEGORY] [-l LIMIT]` |
| `edit` | Update entry | `kb edit <id> [-c CATEGORY] [-t TITLE] [-m CONTENT] [--tags TAGS]` |
| `delete` | Remove entry | `kb delete <id>` |
| `import` | Bulk import notes | `kb import <markdown\|txt> <filepath> [-c CATEGORY]` |
| `export` | Export dataset | `kb export <json\|markdown\|backup> <output> [-c CATEGORY]` |
| `stats` | Display metrics | `kb stats` |
| `favorite`| Toggle favorite | `kb favorite <id> [-l]` |
| `recent` | Recent entries | `kb recent [-l LIMIT]` |
| `copy` | Copy to clipboard | `kb copy <id>` |
