import json
import shutil
from pathlib import Path

from kb.models.knowledge import KnowledgeItem
from kb.services.knowledge_service import KnowledgeService


class ImportExportService:
    """Import and export knowledge base entries."""

    def __init__(self, service: KnowledgeService):
        self.service = service

    def import_markdown_file(
        self,
        file_path: Path,
        category: str | None = None,
    ) -> list[KnowledgeItem]:
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        text = file_path.read_text(encoding="utf-8")

        category = category or file_path.stem.lower()

        items: list[KnowledgeItem] = []

        current_title = file_path.stem
        current_lines: list[str] = []

        for line in text.splitlines():
            if line.startswith("# "):
                if current_lines:
                    content = "\n".join(current_lines).strip()

                    if content:
                        items.append(
                            self.service.add_item(
                                category=category,
                                title=current_title,
                                content=content,
                            )
                        )

                current_title = line[2:].strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            content = "\n".join(current_lines).strip()

            if content:
                items.append(
                    self.service.add_item(
                        category=category,
                        title=current_title,
                        content=content,
                    )
                )

        return items

    def import_txt_file(
        self,
        file_path: Path,
        category: str | None = None,
        title: str | None = None,
    ) -> KnowledgeItem:
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        return self.service.add_item(
            category=category or "general",
            title=title or file_path.stem,
            content=file_path.read_text(encoding="utf-8").strip(),
        )

    def export_json(
        self,
        output_path: Path,
        category: str | None = None,
    ) -> int:
        items = self.service.list_items(
            limit=10000,
            category=category,
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                [
                    {
                        "id": item.id,
                        "category": item.category,
                        "title": item.title,
                        "content": item.content,
                        "tags": item.tags,
                        "favorite": item.favorite,
                        "access_count": item.access_count,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                    }
                    for item in items
                ],
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        return len(items)

    def export_markdown(
        self,
        output_path: Path,
        category: str | None = None,
    ) -> int:
        items = self.service.list_items(
            limit=10000,
            category=category,
        )

        lines = [
            "# Knowledge Base Export",
            "",
        ]

        current_category = None

        for item in items:
            if item.category != current_category:
                current_category = item.category

                lines.extend(
                    [
                        "",
                        f"## {current_category.upper()}",
                        "",
                    ]
                )

            lines.append(f"### {item.title}")

            if item.tags:
                lines.append(f"**Tags:** {item.tags_str}")

            if item.favorite:
                lines.append("**Favorite:** ⭐")

            lines.extend(
                [
                    "",
                    "```text",
                    item.content,
                    "```",
                    "",
                ]
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return len(items)

    def backup_database(
        self,
        source_db: Path,
        backup_path: Path,
    ) -> Path:
        if not source_db.exists():
            raise FileNotFoundError(source_db)

        backup_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_db,
            backup_path,
        )

        return backup_path
