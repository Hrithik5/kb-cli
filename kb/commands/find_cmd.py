import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class FindCommand(BaseCommand):
    name = "find"
    help_text = "Search knowledge base entries using fast SQLite FTS5 full-text search."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("query", nargs="?", default="", help="Search query keywords")
        parser.add_argument("-c", "--category", help="Filter by specific category")
        parser.add_argument("-l", "--limit", type=int, default=10, help="Maximum number of results to display")

    def execute(self, args: argparse.Namespace) -> int:
        limit = args.limit or self.config.default_limit
        items = self.service.find_items(query=args.query, limit=limit, category=args.category)
        print(Formatter.format_items_list(items))
        return 0
