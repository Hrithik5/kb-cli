import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class GetCommand(BaseCommand):
    name = "get"
    help_text = "Display a knowledge item."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "id",
            type=int,
            help="Knowledge item ID",
        )

        parser.add_argument(
            "--pretty",
            action="store_true",
            help="Render a formatted view instead of raw content.",
        )

    def execute(self, args: argparse.Namespace) -> int:
        item = self.service.get_item(
            args.id,
            track_access=False,
        )

        if not item:
            print(
                Formatter.color(
                    f"Snippet #{args.id} not found.",
                    Formatter.RED,
                )
            )
            return 1

        if args.pretty:
            print(
                Formatter.format_item(
                    item,
                    verbose=True,
                )
            )
        else:
            # Used by scripts and fzf preview
            print(item.content)

        return 0
