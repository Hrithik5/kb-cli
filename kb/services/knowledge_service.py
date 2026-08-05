from typing import List, Optional, Union
from kb.models.knowledge import KnowledgeItem
from kb.repositories.knowledge_repository import KnowledgeRepository


class KnowledgeService:
    """Business logic layer for managing knowledge items and search workflows."""

    def __init__(self, repo: KnowledgeRepository):
        self.repo = repo

    def add_item(
        self,
        category: str,
        content: str,
        title: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None
    ) -> KnowledgeItem:
        category = category.strip().lower()
        if not category:
            raise ValueError("Category cannot be empty.")
        content = content.strip()
        if not content:
            raise ValueError("Content cannot be empty.")

        if isinstance(tags, str):
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        elif isinstance(tags, list):
            tag_list = [t.strip() for t in tags if t.strip()]
        else:
            tag_list = []

        item = KnowledgeItem(
            category=category,
            content=content,
            title=title.strip() if title else "",
            tags=tag_list
        )
        return self.repo.add(item)

    def find_items(
        self,
        query: str,
        limit: int = 10,
        category: Optional[str] = None,
        track_access: bool = True
    ) -> List[KnowledgeItem]:
        query = query.strip()
        if not query:
            return self.repo.list_all(limit=limit, category=category)

        items = self.repo.find(query=query, limit=limit, category=category)
        if track_access:
            for item in items:
                if item.id:
                    self.repo.increment_access(item.id)
        return items

    def list_items(self, limit: int = 20, category: Optional[str] = None) -> List[KnowledgeItem]:
        return self.repo.list_all(limit=limit, category=category)

    def get_item(self, item_id: int, track_access: bool = False) -> Optional[KnowledgeItem]:
        item = self.repo.get_by_id(item_id)
        if item and track_access:
            self.repo.increment_access(item_id)
        return item

    def edit_item(
        self,
        item_id: int,
        category: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None
    ) -> KnowledgeItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise ValueError(f"Knowledge item with ID {item_id} not found.")

        if category is not None:
            category_clean = category.strip().lower()
            if category_clean:
                item.category = category_clean
        if title is not None:
            item.title = title.strip()
        if content is not None:
            content_clean = content.strip()
            if content_clean:
                item.content = content_clean
        if tags is not None:
            if isinstance(tags, str):
                item.tags = [t.strip() for t in tags.split(",") if t.strip()]
            elif isinstance(tags, list):
                item.tags = [t.strip() for t in tags if t.strip()]

        return self.repo.update(item)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)

    def toggle_favorite(self, item_id: int) -> Optional[bool]:
        return self.repo.toggle_favorite(item_id)

    def get_recent(self, limit: int = 10) -> List[KnowledgeItem]:
        return self.repo.get_recent(limit=limit)

    def get_favorites(self, limit: int = 20) -> List[KnowledgeItem]:
        return self.repo.get_favorites(limit=limit)

    def get_stats(self) -> dict:
        return self.repo.get_stats()
