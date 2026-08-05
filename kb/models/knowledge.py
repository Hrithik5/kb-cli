from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class KnowledgeItem:
    """Represents a single knowledge snippet/note entry in kb."""
    category: str
    content: str
    title: str = ""
    tags: List[str] = field(default_factory=list)
    id: Optional[int] = None
    favorite: bool = False
    access_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.tags, str):
            # Parse comma-separated string to list if necessary
            self.tags = [t.strip() for t in self.tags.split(",") if t.strip()]
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
        if not self.title:
            # Fallback title if unspecified
            lines = [line.strip() for line in self.content.splitlines() if line.strip()]
            self.title = lines[0][:60] if lines else "Untitled"

    @property
    def tags_str(self) -> str:
        """Returns comma-separated string of tags."""
        return ", ".join(self.tags)
