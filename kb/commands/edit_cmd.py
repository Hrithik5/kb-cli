import argparse
from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class EditCommand(BaseCommand):
    name = "edit"
    help_text = "Edit an existing knowledge base item by ID."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("id", type=int, help="Item ID to edit")
        parser.add_argument("-c", "--category", help="Updated category")
        parser.add_argument("-t", "--title", help="Updated title")
        parser.add_argument("-m", "--content", help="Updated snippet or text content")
        parser.add_argument("--tags", help="Updated comma-separated tags")

    def execute(self, args: argparse.Namespace) -> int:
        try:
            item = self.service.edit_item(
                item_id=args.id,
                category=args.category,
                title=args.title,
                content=args.content,
                tags=args.tags
            )
            print(Formatter.color(f"✔ Updated #{item.id} [{item.category}] {item.title}", Formatter.GREEN))
            return 0
        except ValueError as e:
            print(Formatter.color(f"Error: {e}", Formatter.RED))
            return 1
