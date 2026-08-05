import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class EditCommand(BaseCommand):
    name = "edit"
    help_text = "Edit an existing knowledge base item."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "id",
            type=int,
            help="Knowledge item ID",
        )

        parser.add_argument(
            "-c",
            "--category",
            help="New category",
        )

        parser.add_argument(
            "-t",
            "--title",
            help="New title",
        )

        parser.add_argument(
            "-m",
            "--content",
            help="New snippet content",
        )

        parser.add_argument(
            "--tags",
            help="Comma-separated tags",
        )

    def execute(self, args: argparse.Namespace) -> int:
        if (
            args.category is None
            and args.title is None
            and args.content is None
            and args.tags is None
        ):
            print(
                Formatter.color(
                    "Nothing to update. Specify at least one field.",
                    Formatter.YELLOW,
                )
            )
            return 1

        try:
            item = self.service.edit_item(
                item_id=args.id,
                category=args.category,
                title=args.title,
                content=args.content,
                tags=args.tags,
            )

            print(
                Formatter.color(
                    f"✔ Updated #{item.id}",
                    Formatter.GREEN,
                )
            )

            print(
                Formatter.format_item(
                    item,
                    verbose=True,
                )
            )

            return 0

        except ValueError as exc:
            print(
                Formatter.color(
                    f"Error: {exc}",
                    Formatter.RED,
                )
            )
            return 1
