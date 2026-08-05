import json
import shutil
from pathlib import Path

from kb.models.knowledge import KnowledgeItem
from kb.services.knowledge_service import KnowledgeService


class ImportExportService:
    """Handles importing and exporting knowledge base entries across formats."""

    def __init__(self, service: KnowledgeService):
        self.service = service

    def import_markdown_file(self, file_path: Path, category: str | None = None) -> list[KnowledgeItem]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        text = file_path.read_text(encoding="utf-8")
        cat = category or file_path.stem.lower()

        # Parse sections or headers (# Title)
        items = []
        current_title = file_path.stem
        current_lines = []

        for line in text.splitlines():
            if line.startswith("# "):
                if current_lines:
                    content = "\n".join(current_lines).strip()
                    if content:
                        item = self.service.add_item(category=cat, content=content, title=current_title)
                        items.append(item)
                    current_lines = []
                current_title = line[2:].strip()
            else:
                current_lines.append(line)

        if current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                item = self.service.add_item(category=cat, content=content, title=current_title)
                items.append(item)

        return items

    def import_txt_file(self, file_path: Path, category: str | None = None, title: str | None = None) -> KnowledgeItem:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8").strip()
        cat = category or "general"
        t = title or file_path.stem

        return self.service.add_item(category=cat, content=content, title=t)

    def export_json(self, output_path: Path, category: str | None = None) -> int:
        items = self.service.list_items(limit=10000, category=category)
        data = [
            {
                "id": item.id,
                "category": item.category,
                "title": item.title,
                "content": item.content,
                "tags": item.tags,
                "favorite": item.favorite,
                "access_count": item.access_count,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
            for item in items
        ]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return len(items)

    def export_markdown(self, output_path: Path, category: str | None = None) -> int:
        items = self.service.list_items(limit=10000, category=category)
        md_lines = ["# Knowledge Base Export\n"]

        current_cat = None
        for item in items:
            if item.category != current_cat:
                current_cat = item.category
                md_lines.append(f"\n## Category: {current_cat.upper()}\n")

            md_lines.append(f"### {item.title}")
            if item.tags:
                md_lines.append(f"*Tags: {item.tags_str}*\n")
            md_lines.append(f"```\n{item.content}\n```\n")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(md_lines), encoding="utf-8")
        return len(items)

    def backup_database(self, source_db: Path, backup_path: Path) -> Path:
        if not source_db.exists():
            raise FileNotFoundError(f"Source database not found: {source_db}")
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_db, backup_path)
        return backup_path
