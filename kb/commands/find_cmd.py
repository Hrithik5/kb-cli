import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class FindCommand(BaseCommand):
    name = "find"
    help_text = "Search knowledge base entries using SQLite FTS5."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "query",
            nargs="?",
            default="",
            help="Search query keywords",
        )
        parser.add_argument(
            "-c",
            "--category",
            help="Filter by category",
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            default=10,
            help="Maximum number of results",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Show additional metadata",
        )

    def execute(self, args: argparse.Namespace) -> int:
        limit = args.limit or self.config.default_limit

        items = self.service.find_items(
            query=args.query,
            limit=limit,
            category=args.category,
        )

        print(
            Formatter.format_items_list(
                items,
                query=args.query,
            )
        )

        return 0
