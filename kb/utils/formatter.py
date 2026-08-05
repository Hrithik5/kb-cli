import sys
from typing import List
from kb.models.knowledge import KnowledgeItem


class Formatter:
    """Terminal output formatter with ANSI color support."""

    # ANSI Colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    RED = "\033[31m"

    @classmethod
    def _supports_color(cls) -> bool:
        return sys.stdout.isatty()

    @classmethod
    def color(cls, text: str, color_code: str) -> str:
        if cls._supports_color():
            return f"{color_code}{text}{cls.RESET}"
        return text

    @classmethod
    def format_item(cls, item: KnowledgeItem, verbose: bool = False) -> str:
        fav = " ★" if item.favorite else ""
        category_tag = cls.color(f"[{item.category.upper()}]", cls.CYAN + cls.BOLD)
        title_str = cls.color(f"{item.title}{fav}", cls.BOLD)
        id_str = cls.color(f"#{item.id}", cls.DIM)

        lines = [f"{id_str} {category_tag} {title_str}"]

        if item.tags:
            tags_fmt = cls.color(f"tags: {item.tags_str}", cls.YELLOW)
            lines.append(f"   {tags_fmt}")

        content_lines = item.content.splitlines()
        for line in content_lines:
            lines.append(f"   {line}")

        if verbose:
            lines.append(cls.color(f"   (Created: {item.created_at} | Views: {item.access_count})", cls.DIM))

        return "\n".join(lines)

    @classmethod
    def format_items_list(cls, items: List[KnowledgeItem]) -> str:
        if not items:
            return cls.color("No matches found.", cls.YELLOW)

        output = [cls.color(f"Found {len(items)} match{'es' if len(items) != 1 else ''}:\n", cls.BOLD)]
        for item in items:
            output.append(cls.format_item(item))
            output.append("")  # Empty spacing line

        return "\n".join(output).strip()

    @classmethod
    def format_stats(cls, stats: dict) -> str:
        total = stats.get("total_items", 0)
        favs = stats.get("favorite_items", 0)
        cats = stats.get("categories", {})
        most_acc = stats.get("most_accessed", [])

        output = [
            cls.color("=== Knowledge Base Statistics ===", cls.BOLD + cls.CYAN),
            f"Total Snippets:  {cls.color(str(total), cls.BOLD)}",
            f"Favorites:       {cls.color(str(favs), cls.YELLOW)}",
            f"Categories:      {len(cats)}",
            ""
        ]

        if cats:
            output.append(cls.color("Categories Breakdown:", cls.BOLD))
            for cat, count in cats.items():
                output.append(f"  • {cat.ljust(15)} : {count}")
            output.append("")

        if most_acc:
            output.append(cls.color("Top Accessed Items:", cls.BOLD))
            for item in most_acc:
                output.append(f"  • #{item.id} [{item.category}] {item.title} ({item.access_count} views)")

        return "\n".join(output)
