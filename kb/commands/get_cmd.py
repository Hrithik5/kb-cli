import argparse

from kb.commands.base import BaseCommand


class GetCommand(BaseCommand):
    name = "get"
    help_text = "Get raw content of a knowledge item by ID (scripting/fzf helper)."

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("id", type=int, help="Knowledge item ID")

    def execute(self, args: argparse.Namespace) -> int:
        item = self.service.get_item(args.id, track_access=False)
        if not item:
            return 1
        print(item.content)
        return 0
