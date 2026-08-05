import argparse

from kb.commands.base import BaseCommand
from kb.utils.formatter import Formatter


class DeleteCommand(BaseCommand):
    name = "delete"
    help_text = "Delete a knowledge base item by ID."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("id", type=int, help="Item ID to delete")

    def execute(self, args: argparse.Namespace) -> int:
        success = self.service.delete_item(args.id)
        if success:
            print(Formatter.color(f"✔ Deleted entry #{args.id}", Formatter.GREEN))
            return 0
        else:
            print(Formatter.color(f"Error: Item #{args.id} not found.", Formatter.RED))
            return 1
