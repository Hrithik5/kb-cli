from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class KnowledgeItem:
    """Represents a single knowledge snippet/note entry in kb."""

    category: str
    content: str
    title: str = ""
    tags: list[str] = field(default_factory=list)
    id: int | None = None
    favorite: bool = False
    access_count: int = 0
    created_at: str | None = None
    updated_at: str | None = None

    def __post_init__(self):
        if isinstance(self.tags, str):
            # Parse comma-separated string to list if necessary
            self.tags = [t.strip() for t in self.tags.split(",") if t.strip()]

        now = datetime.now(UTC).isoformat()

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
