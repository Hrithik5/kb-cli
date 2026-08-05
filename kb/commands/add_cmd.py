import argparse
from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class AddCommand(BaseCommand):
    name = "add"
    help_text = "Add a new knowledge entry or command snippet."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("category", help="Category for the item (e.g. git, docker, python)")
        parser.add_argument("content", help="Snippet or text content")
        parser.add_argument("-t", "--title", default="", help="Optional title for the snippet")
        parser.add_argument("--tags", default="", help="Comma-separated tags (e.g. 'git,branch,delete')")

    def execute(self, args: argparse.Namespace) -> int:
        try:
            item = self.service.add_item(
                category=args.category,
                content=args.content,
                title=args.title,
                tags=args.tags
            )
            print(Formatter.color(f"✔ Added #{item.id} [{item.category}] {item.title}", Formatter.GREEN))
            return 0
        except ValueError as e:
            print(Formatter.color(f"Error: {e}", Formatter.RED))
            return 1
