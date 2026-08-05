import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class RecentCommand(BaseCommand):
    name = "recent"
    help_text = "Show recently added or updated knowledge entries."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-l", "--limit", type=int, default=10, help="Number of recent items to list")

    def execute(self, args: argparse.Namespace) -> int:
        items = self.service.get_recent(limit=args.limit)
        print(Formatter.format_items_list(items))
        return 0
