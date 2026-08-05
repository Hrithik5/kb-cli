from kb.models.knowledge import KnowledgeItem
from kb.repositories.knowledge_repository import KnowledgeRepository


class KnowledgeService:
    """Business logic layer for managing knowledge items."""

    def __init__(self, repo: KnowledgeRepository):
        self.repo = repo

    @staticmethod
    def _normalize_tags(
        tags: list[str] | str | None,
    ) -> list[str]:
        if tags is None:
            return []

        if isinstance(tags, str):
            values = tags.split(",")
        else:
            values = tags

        seen: set[str] = set()
        normalized: list[str] = []

        for tag in values:
            clean = tag.strip().lower()
            if clean and clean not in seen:
                seen.add(clean)
                normalized.append(clean)

        return normalized

    def add_item(
        self,
        category: str,
        content: str,
        title: str | None = None,
        tags: list[str] | str | None = None,
    ) -> KnowledgeItem:
        category = category.strip().lower()

        if not category:
            raise ValueError("Category cannot be empty.")

        content = content.strip()

        if not content:
            raise ValueError("Content cannot be empty.")

        item = KnowledgeItem(
            category=category,
            content=content,
            title=title.strip() if title else "",
            tags=self._normalize_tags(tags),
        )

        return self.repo.add(item)

    def find_items(
        self,
        query: str,
        limit: int = 10,
        category: str | None = None,
        track_access: bool = True,
    ) -> list[KnowledgeItem]:
        query = query.strip()

        if not query:
            items = self.repo.list_all(
                limit=limit,
                category=category,
            )
        else:
            items = self.repo.find(
                query=query,
                limit=limit,
                category=category,
            )

        if track_access:
            seen: set[int] = set()

            for item in items:
                if item.id is not None and item.id not in seen:
                    self.repo.increment_access(item.id)
                    seen.add(item.id)

        return items

    def list_items(
        self,
        limit: int = 20,
        category: str | None = None,
    ) -> list[KnowledgeItem]:
        return self.repo.list_all(
            limit=limit,
            category=category,
        )

    def get_item(
        self,
        item_id: int,
        track_access: bool = False,
    ) -> KnowledgeItem | None:
        item = self.repo.get_by_id(item_id)

        if item and track_access:
            self.repo.increment_access(item_id)

        return item

    def edit_item(
        self,
        item_id: int,
        category: str | None = None,
        title: str | None = None,
        content: str | None = None,
        tags: list[str] | str | None = None,
    ) -> KnowledgeItem:
        item = self.repo.get_by_id(item_id)

        if item is None:
            raise ValueError(f"Knowledge item with ID {item_id} not found.")

        if category is not None:
            category = category.strip().lower()
            if category:
                item.category = category

        if title is not None:
            item.title = title.strip()

        if content is not None:
            content = content.strip()
            if content:
                item.content = content

        if tags is not None:
            item.tags = self._normalize_tags(tags)

        return self.repo.update(item)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)

    def toggle_favorite(
        self,
        item_id: int,
    ) -> bool | None:
        return self.repo.toggle_favorite(item_id)

    def get_recent(
        self,
        limit: int = 10,
    ) -> list[KnowledgeItem]:
        return self.repo.get_recent(limit=limit)

    def get_favorites(
        self,
        limit: int = 20,
    ) -> list[KnowledgeItem]:
        return self.repo.get_favorites(limit=limit)

    def get_stats(self) -> dict:
        return self.repo.get_stats()
