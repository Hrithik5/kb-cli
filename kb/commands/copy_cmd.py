import argparse
from kb.commands.base import BaseCommand
from kb.utils.clipboard import copy_to_clipboard
from kb.utils.formatter import Formatter


class CopyCommand(BaseCommand):
    name = "copy"
    help_text = "Copy snippet content of an entry to system clipboard."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("id", type=int, help="Item ID to copy")

    def execute(self, args: argparse.Namespace) -> int:
        item = self.service.get_item(args.id, track_access=True)
        if not item:
            print(Formatter.color(f"Error: Item #{args.id} not found.", Formatter.RED))
            return 1

        success = copy_to_clipboard(item.content)
        if success:
            print(Formatter.color(f"✔ Copied snippet #{item.id} to clipboard!", Formatter.GREEN))
        else:
            print(Formatter.color(f"Content of #{item.id}:\n{item.content}", Formatter.CYAN))
        return 0
