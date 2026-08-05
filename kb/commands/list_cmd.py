import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class ListCommand(BaseCommand):
    name = "list"
    help_text = "List knowledge base items."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-c", "--category", help="Filter by specific category")
        parser.add_argument(
            "-l", "--limit", type=int, default=20, help="Maximum items to list"
        )

    def execute(self, args: argparse.Namespace) -> int:
        items = self.service.list_items(limit=args.limit, category=args.category)
        print(Formatter.format_items_list(items))
        return 0
