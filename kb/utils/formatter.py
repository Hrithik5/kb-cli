import re
import shutil
import sys

from kb.models.knowledge import KnowledgeItem


class Formatter:
    """Rich terminal renderer used across kb."""

    # --------------------------
    # ANSI Colors
    # --------------------------

    RESET = "\033[0m"

    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[97m"

    # Unicode

    STAR = "★"
    BULLET = "•"

    # --------------------------

    @classmethod
    def _supports_color(cls) -> bool:
        return sys.stdout.isatty()

    @classmethod
    def color(cls, text: str, color: str) -> str:
        if cls._supports_color():
            return f"{color}{text}{cls.RESET}"
        return text

    @classmethod
    def terminal_width(cls) -> int:
        return shutil.get_terminal_size((100, 20)).columns

    @classmethod
    def divider(cls) -> str:
        return "─" * min(cls.terminal_width(), 100)

    # ---------------------------------------------------
    # Highlight Search Matches
    # ---------------------------------------------------

    @classmethod
    def highlight(cls, text: str, query: str | None) -> str:
        if not query:
            return text

        result = text

        for token in query.split():
            if not token.strip():
                continue

            pattern = re.compile(re.escape(token), re.IGNORECASE)

            result = pattern.sub(
                lambda m: cls.color(m.group(0), cls.BOLD + cls.YELLOW),
                result,
            )

        return result

    # ---------------------------------------------------
    # Rich Knowledge Card
    # ---------------------------------------------------

    @classmethod
    def format_item(
        cls,
        item: KnowledgeItem,
        query: str | None = None,
        verbose: bool = False,
    ) -> str:

        star = cls.color(f"{cls.STAR} Favorite", cls.YELLOW) if item.favorite else ""

        title = cls.highlight(item.title, query)
        content = cls.highlight(item.content, query)

        tags = cls.highlight(item.tags_str, query) if item.tags else "-"

        header = (
            f"{cls.color(f'#{item.id}', cls.DIM)}   "
            f"{cls.color(item.category.upper(), cls.CYAN + cls.BOLD)}"
        )

        if star:
            header += f"   {star}"

        lines = [
            cls.divider(),
            header,
            "",
            f"{cls.color('Title', cls.BOLD)}      {title}",
            f"{cls.color('Tags', cls.BOLD)}       {tags}",
        ]

        if verbose:
            lines.extend(
                [
                    f"{cls.color('Updated', cls.BOLD)}    {item.updated_at}",
                    f"{cls.color('Views', cls.BOLD)}      {item.access_count}",
                ]
            )

        lines.extend(
            [
                "",
                cls.color("Snippet", cls.BOLD),
                content,
                cls.divider(),
            ]
        )

        return "\n".join(lines)

    # ---------------------------------------------------
    # Multiple Results
    # ---------------------------------------------------

    @classmethod
    def format_items_list(
        cls,
        items: list[KnowledgeItem],
        query: str | None = None,
    ) -> str:

        if not items:
            return cls.color("No matching snippets found.", cls.YELLOW)

        output = [
            cls.color(
                f"{len(items)} result{'s' if len(items) != 1 else ''}",
                cls.BOLD + cls.GREEN,
            ),
            "",
        ]

        for item in items:
            output.append(cls.format_item(item, query=query))
            output.append("")

        return "\n".join(output).rstrip()

    # ---------------------------------------------------
    # Statistics
    # ---------------------------------------------------

    @classmethod
    def format_stats(cls, stats: dict) -> str:

        total = stats.get("total_items", 0)
        favs = stats.get("favorite_items", 0)
        cats = stats.get("categories", {})
        top = stats.get("most_accessed", [])

        out = [
            cls.divider(),
            cls.color("Knowledge Base Statistics", cls.BOLD + cls.CYAN),
            cls.divider(),
            "",
            f"Total Snippets : {cls.color(str(total), cls.BOLD)}",
            f"Favorites      : {cls.color(str(favs), cls.YELLOW)}",
            f"Categories     : {len(cats)}",
            "",
        ]

        if cats:
            out.append(cls.color("Categories", cls.BOLD))

            for cat, count in cats.items():
                out.append(f"  {cls.BULLET} {cat:<18} {count}")

            out.append("")

        if top:
            out.append(cls.color("Most Accessed", cls.BOLD))

            for item in top:
                out.append(
                    f"  {cls.BULLET} #{item.id} {item.title} ({item.access_count})"
                )

        out.append(cls.divider())

        return "\n".join(out)
