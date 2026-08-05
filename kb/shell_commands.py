import os
import subprocess
import tempfile
from pathlib import Path

from kb.services.knowledge_service import KnowledgeService
from kb.utils.formatter import Formatter


class ShellCommands:
    """Interactive commands used by the kb shell."""

    def __init__(self, service: KnowledgeService, editor: str):
        self.service = service
        self.editor = editor

    def help(self) -> None:
        print(
            """
Available Commands

General
-------
help, ?              Show this help
exit, quit, q        Exit shell

Search
------
list, ls             List snippets
find <query>         Search snippets
get <id>             View snippet
recent               Show recent snippets
favorites            List favorites
stats                Show statistics

Manage
------
add                  Add new snippet
edit <id>            Edit snippet
favorite <id>        Toggle favorite
delete <id>          Delete snippet
"""
        )

    def list(self) -> None:
        print(Formatter.format_items_list(self.service.list_items(limit=20)))

    def recent(self) -> None:
        print(Formatter.format_items_list(self.service.get_recent()))

    def favorites(self) -> None:
        print(Formatter.format_items_list(self.service.get_favorites()))

    def stats(self) -> None:
        print(Formatter.format_stats(self.service.get_stats()))

    def find(self, query: str) -> None:
        print(Formatter.format_items_list(self.service.find_items(query=query)))

    def get(self, item_id: int) -> None:
        item = self.service.get_item(
            item_id,
            track_access=True,
        )

        if item is None:
            print(
                Formatter.color(
                    "Snippet not found.",
                    Formatter.RED,
                )
            )
            return

        print(
            Formatter.format_item(
                item,
                verbose=True,
            )
        )

    def add(self) -> None:
        print()

        category = input("Category : ").strip()
        title = input("Title    : ").strip()

        print("\nPaste snippet below.")
        print("Press Ctrl+D when finished.\n")

        lines: list[str] = []

        try:
            while True:
                lines.append(input())
        except EOFError:
            print()

        content = "\n".join(lines).strip()
        tags = input("Tags     : ").strip()

        try:
            item = self.service.add_item(
                category=category,
                title=title,
                content=content,
                tags=tags,
            )

            print(
                Formatter.color(
                    f"✔ Added #{item.id}",
                    Formatter.GREEN,
                )
            )

        except ValueError as exc:
            print(
                Formatter.color(
                    str(exc),
                    Formatter.RED,
                )
            )

    def edit(self, item_id: int) -> None:
        """Edit a snippet using the configured editor."""

        item = self.service.get_item(item_id)

        if item is None:
            print(
                Formatter.color(
                    "Snippet not found.",
                    Formatter.RED,
                )
            )
            return

        initial_text = f"""# Edit the fields below.
# Lines beginning with # are ignored.

Category: {item.category}
Title: {item.title}
Tags: {item.tags_str}

---

{item.content}
"""

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(initial_text)
            temp_path = Path(tmp.name)

        editor = self.editor or os.environ.get("EDITOR") or "vi"

        try:
            subprocess.run(
                [editor, str(temp_path)],
                check=True,
            )

            text = temp_path.read_text(
                encoding="utf-8",
            )

        finally:
            if temp_path.exists():
                temp_path.unlink()

        lines = [line for line in text.splitlines() if not line.startswith("#")]

        try:
            separator = lines.index("---")
        except ValueError:
            print(
                Formatter.color(
                    "Invalid edit format.",
                    Formatter.RED,
                )
            )
            return

        metadata = lines[:separator]
        content = "\n".join(lines[separator + 1 :]).strip()

        values: dict[str, str] = {}

        for line in metadata:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            values[key.strip().lower()] = value.strip()

        try:
            updated = self.service.edit_item(
                item_id=item_id,
                category=values.get("category"),
                title=values.get("title"),
                tags=values.get("tags"),
                content=content,
            )

            print(
                Formatter.color(
                    f"✔ Updated #{updated.id}",
                    Formatter.GREEN,
                )
            )

        except ValueError as exc:
            print(
                Formatter.color(
                    str(exc),
                    Formatter.RED,
                )
            )

    def delete(self, item_id: int) -> None:
        item = self.service.get_item(item_id)

        if item is None:
            print(
                Formatter.color(
                    "Snippet not found.",
                    Formatter.RED,
                )
            )
            return

        confirm = input(f'Delete "{item.title}"? [y/N]: ').strip().lower()

        if confirm != "y":
            print("Cancelled.")
            return

        self.service.delete_item(item_id)

        print(
            Formatter.color(
                "Deleted.",
                Formatter.GREEN,
            )
        )

    def favorite(self, item_id: int) -> None:
        status = self.service.toggle_favorite(item_id)

        if status is None:
            print(
                Formatter.color(
                    "Snippet not found.",
                    Formatter.RED,
                )
            )
            return

        if status:
            print(
                Formatter.color(
                    "★ Marked as favorite.",
                    Formatter.YELLOW,
                )
            )
        else:
            print(
                Formatter.color(
                    "Removed from favorites.",
                    Formatter.DIM,
                )
            )
